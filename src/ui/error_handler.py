class ErrorHandler:
    def __init__(self, parent=None):
        self.parent = parent  # ventana padre para mensajes

    def handle(self, e: Exception):
        # Aquí puedes filtrar excepciones, loggear, etc
        import traceback
        print(f"Error capturado: {e}")
        traceback.print_exc()

        # Ejemplo simple de diferentes reacciones:
        if isinstance(e, ValueError):
            self.show_message("Error de valor", str(e))
        elif isinstance(e, FileNotFoundError):
            self.show_message("Archivo no encontrado", str(e))
        else:
            # Error crítico, mostrar y cerrar app si quieres
            self.show_message("Error crítico", str(e))
            import sys
            sys.exit(1)

    def show_message(self, title, message):
        from PySide6.QtWidgets import QMessageBox
        dlg = QMessageBox(self.parent)
        dlg.setWindowTitle(title)
        dlg.setIcon(QMessageBox.Critical)
        dlg.setText(message)
        dlg.exec()
