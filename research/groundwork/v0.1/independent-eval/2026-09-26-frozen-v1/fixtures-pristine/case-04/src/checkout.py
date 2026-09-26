def checkout(order, bus):
    bus.publish("order.paid", {"id": order.id})
    return {"status": "accepted"}
