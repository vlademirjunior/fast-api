from app.schemas.user import User, TokenData
import pytest
from datetime import datetime

def test_user_schema():
    user = User(username='vlad', password='!2e')
    assert user.model_dump() == {
        'username': 'vlad', 'password': '!2e'
    }

def test_user_schema_inalid_username():
    with pytest.raises(ValueError):
        User(username='v!ad', password='!2e')


def test_token_data():
    expires_at = datetime.now()
    token_data = TokenData(
        access_token='token qualquer',
        expires_at=expires_at
    )

    assert token_data.model_dump() == {
        'access_token': 'token qualquer',
        'expires_at': expires_at
    }