from bowen_clinic import app

if __name__ == '__main__':
    app.jinja_env.cache = {}
    # bowen clinic: host="192.168.31.66"
    app.run(host="192.168.31.66", port=5000, debug=True)