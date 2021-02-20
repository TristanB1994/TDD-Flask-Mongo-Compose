from manage import configure_env, setenv
# from application.wsgi import app
import pytest

@pytest.mark.parametrize("env, ", ['testing','development','production'])
def test_configure_env(env):

    setenv('FLASK_CONFIG', env)

    from application.wsgi import app
    print(f"env: {env}")

    assert app.config['USER_APP_NAME'] == 'Registry'            