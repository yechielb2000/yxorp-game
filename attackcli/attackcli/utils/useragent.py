from fake_useragent import UserAgent

_user_agent = UserAgent(platforms=["desktop"])


def get_random_user_agent():
    return _user_agent.random
