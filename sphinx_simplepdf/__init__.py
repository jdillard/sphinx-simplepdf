from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from sphinx.util import logging

from sphinx_simplepdf.directives.ifbuilder import IfBuilderDirective
from sphinx_simplepdf.directives.ifinclude import IfIncludeDirective
from sphinx_simplepdf.directives.pdfinclude import PdfIncludeDirective

logger = logging.getLogger(__name__)


class _PdfGenerator:
    """Manages an optional parallel simplepdf subprocess build."""

    def __init__(self, app):
        self.app = app
        self.process = None
        self.build_dir = None
        self.log_path = None

    def _on_builder_inited(self, app):
        if app.builder.name == "simplepdf":
            return
        if not app.config.simplepdf_build_parallel:
            return

        self._start_subprocess(app)

    def _on_build_finished(self, app, exception):
        if app.builder.name == "simplepdf":
            return
        if not app.config.simplepdf_build_parallel:
            return

        if exception:
            logger.warning("sphinx-simplepdf: skipping PDF due to build error")
            self._cleanup()
            return

        if self.process is None:
            return

        if self.process.poll() is None:
            logger.info("sphinx-simplepdf: waiting for PDF build to finish...")
        self.process.wait()

        if self.process.returncode != 0:
            log_hint = f"  see log: {self.log_path}" if self.log_path else ""
            logger.warning(
                f"sphinx-simplepdf: PDF build failed (exit {self.process.returncode}){log_hint}"
            )
            self._cleanup()
            return

        self._copy_pdf(app)
        self._cleanup()

    def _start_subprocess(self, app):
        self.build_dir = Path(tempfile.mkdtemp(prefix="simplepdf_"))
        self.log_path = self.build_dir / "build.log"

        cmd = [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "simplepdf",
            str(app.srcdir),
            str(self.build_dir / "output"),
            "-d",
            str(self.build_dir / "doctrees"),
            "-q",
        ]

        logger.info("sphinx-simplepdf: starting PDF build subprocess")
        log_fh = self.log_path.open("w")
        self.process = subprocess.Popen(cmd, stdout=log_fh, stderr=subprocess.STDOUT)

    def _copy_pdf(self, app):
        if self.build_dir is None:
            return

        output_dir = self.build_dir / "output"
        pdf_files = list(output_dir.glob("*.pdf"))

        if not pdf_files:
            logger.warning("sphinx-simplepdf: no PDF found in build output")
            return

        dest = Path(app.outdir)
        for pdf in pdf_files:
            target = dest / pdf.name
            shutil.copy2(pdf, target)
            logger.info(f"sphinx-simplepdf: {pdf.name} -> {target}")

    def _cleanup(self):
        if self.build_dir is not None and self.build_dir.exists():
            shutil.rmtree(self.build_dir, ignore_errors=True)
            self.build_dir = None


def setup(app):
    app.add_directive("if-builder", IfBuilderDirective)
    app.add_directive("if-include", IfIncludeDirective)
    app.add_directive("pdf-include", PdfIncludeDirective)

    app.add_config_value("simplepdf_build_parallel", False, "env", types=[bool])

    gen = _PdfGenerator(app)
    app.connect("builder-inited", gen._on_builder_inited)
    app.connect("build-finished", gen._on_build_finished, priority=101)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
