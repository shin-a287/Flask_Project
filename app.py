from flask import Flask, jsonify, redirect, render_template, request, url_for


def create_app(testing=False):
    """Фабрика приложения: удобно создавать отдельный экземпляр для тестов."""
    app = Flask(__name__)
    app.config["TESTING"] = testing

    # Хранилище в памяти (для обучения; после перезапуска данные сбрасываются)
    notes = []

    # ---------- HTML-страницы ----------
    @app.route("/")
    def index():
        return render_template("index.html", notes=notes)

    @app.route("/add", methods=["POST"])
    def add_note():
        text = request.form.get("text", "").strip()
        if text:
            notes.append(text)
        return redirect(url_for("index"))

    @app.route("/about")
    def about():
        return render_template("about.html")

    # ---------- JSON API ----------
    @app.route("/health")
    def health():
        return jsonify(status="ok")

    @app.route("/api/notes", methods=["GET"])
    def api_get_notes():
        return jsonify(notes=notes, count=len(notes))

    @app.route("/api/notes", methods=["POST"])
    def api_add_note():
        data = request.get_json(silent=True) or {}
        text = str(data.get("text", "")).strip()
        if not text:
            return jsonify(error="Поле 'text' обязательно"), 400
        notes.append(text)
        return jsonify(message="Заметка добавлена", text=text), 201

    # ---------- Обработка ошибок ----------
    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
