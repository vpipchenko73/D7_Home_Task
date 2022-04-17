import redis
import time

# a=()
# a=[x*2 for x in range (0,10)]
# print(a)
#
# z={}
# z[1] = z.get(1, []) + [345]
# z[1] = z.get(1, []) + [555]
#
# z[2] = z.get(2, []) + [345]
# z[3] = z.get(3, []) + [555]
#
# print(z)

red=redis.Redis(
    host='redis-18486.c257.us-east-1-3.ec2.cloud.redislabs.com',
    port=18486,
    password='a1M0Vq8pflPo2j56o9gYUE7Ft9ive73v'
)

def hello():
    time.sleep(30)
    print("Hello, world!")

hello()