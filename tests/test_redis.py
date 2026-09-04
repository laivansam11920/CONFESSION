from app.extensions.redis_ext import r

r.set("f", "value")
print(r.get("f"))
