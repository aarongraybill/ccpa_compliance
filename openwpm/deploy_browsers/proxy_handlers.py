from dotenv import dotenv_values
import os.path

def create_oxylab_proxies(geography: str = "st-us_california", proxy_config_file: str = '../../proxy_config.env'):

    proxy_config = dotenv_values(proxy_config_file)

    required_configs = ['OXYLABS_USER','OXYLABS_PASSWORD']
    
    # Check that file exists
    if os.path.isfile(proxy_config_file) is False:
        Warning(f"The file {proxy_config_file} does not exist. Resorting to no proxy...")
        return None
    # check that all required configs are present
    if all(config in proxy_config for config in required_configs) is False:
        Warning(f"One or more of {*required_configs,} is not present in {proxy_config_file}. Resorting to no proxy...")
        return None
    else:
        proxies = {
            "http": f"http://customer-{proxy_config['OXYLABS_USER']}-{geography}:{proxy_config['OXYLABS_PASSWORD']}@pr.oxylabs.io:7777",
            "https": f"http://customer-{proxy_config['OXYLABS_USER']}-{geography}:{proxy_config['OXYLABS_PASSWORD']}@pr.oxylabs.io:7777",
        }
        return proxies

def create_proxies(proxy_provider: str, **kwargs):
    if proxy_provider == 'oxylabs':
        return create_oxylab_proxies(**kwargs)
    else:
        raise ValueError(f"Proxy Provider: \"{proxy_provider}\" is not (currently) supported")