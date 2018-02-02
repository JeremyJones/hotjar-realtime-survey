#from memcache import Client as memcached
from pylibmc import Client as memcached

mc = memcached(['127.0.0.1:11211'])
#mc = memcached(['/tmp/memcached.sock'])
