import os
import sys
import uuid
import subprocess
import threading
import minecraft_launcher_lib
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox

# Если у тебя PyQt5 — замени PyQt6 на PyQt5 в строке выше и в импортах ниже
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox

def run_minecraft(window, nick_input, log_area, btn):
    """Эта функция делает всю работу: ставит и запускает Minecraft"""
    username = nick_input.text().strip()
    if not username:
        log_area.append("❌ Ошибка: введите ник!")
        QMessageBox.warning(window, "Ошибка", "Пожалуйста, введите ник.")
        btn.setEnabled(True)
        return

    # Папка для игры
    base_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
    custom_dir = os.path.join(os.path.dirname(base_dir), ".mnewlauncher")

    log_area.append(f"📁 Папка игры: {custom_dir}")
    if not os.path.exists(custom_dir):
        log_area.append("📂 Создаю папку...")
        os.makedirs(custom_dir)

    version = "1.12.2"
    log_area.append(f"⬇️ Начинаю установку версии {version}...")

    try:
        minecraft_launcher_lib.install.install_minecraft_version(version, custom_dir)
        log_area.append("✅ Версия установлена.")
    except Exception as e:
        log_area.append(f"❌ Ошибка установки: {e}")
        QMessageBox.critical(window, "Ошибка установки", str(e))
        btn.setEnabled(True)
        return

    options = {
        "username": username,
        "uuid": str(uuid.uuid4()),
        "token": "",
        "allow_offline_login": True
    }

    log_area.append("🚀 Формирую команду запуска...")
    command = minecraft_launcher_lib.command.get_minecraft_command(version, custom_dir, options)
    log_area.append("🎮 Запускаю Minecraft...")

    try:
        # Запуск игры
        subprocess.call(command, cwd=custom_dir)
        log_area.append("👋 Minecraft завершён.")
    except Exception as e:
        log_area.append(f"❌ Ошибка запуска: {e}")
        QMessageBox.critical(window, "Ошибка запуска", str(e))

    btn.setEnabled(True)  # Возвращаем кнопку в рабочее состояние


def on_launch_click(window, nick_input, log_area, btn):
    """Обёртка, чтобы запустить работу в отдельном потоке и не заморозить окно"""
    btn.setText("⏳ Идёт запуск…")
    btn.setEnabled(False)
    # Запускаем тяжёлую работу в отдельном потоке — окно не зависнет
    t = threading.Thread(target=run_minecraft, args=(window, nick_input, log_area, btn), daemon=True)
    t.start()


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой лаунчер Minecraft 1.12.2")
        self.setMinimumSize(450, 350)

        # Элементы
        self.nick_input = QLineEdit()
        self.nick_input.setPlaceholderText("Введи ник")
        self.nick_input_2 = QLineEdit()
        self.nick_input_2.setPlaceholderText("введи")
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        self.launch_btn = QPushButton("Запустить Minecraft 1.12.2")

        # Компоновка (как элементы стоят на окне)
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Ник:"))
        top_layout.addWidget(self.nick_input, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.launch_btn)
        main_layout.addWidget(QLabel("Лог (что происходит):"))
        main_layout.addWidget(self.log_area, 1)

        self.setLayout(main_layout)

        # Привязка кнопки к действию
        self.launch_btn.clicked.connect(
            lambda: on_launch_click(self, self.nick_input, self.log_area, self.launch_btn)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())