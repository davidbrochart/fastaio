import pytest

from anyio import connect_tcp, create_task_group
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastaio import Component
from fastaio.web.fastapi import FastAPIComponent

pytestmark = pytest.mark.anyio


async def test_web():
    while True:
        try:
            await connect_tcp("127.0.0.1", 8000)
        except OSError:
            break

    class Subcomponent0(Component):
        async def prepare(self):
            self.app = await self.get_resource(FastAPI)
            self.done()

        async def start(self):
            @self.app.get("/")
            def read_root():
                return {"Hello": "World"}

            self.done()

    class Component0(Component):
        def __init__(self, name):
            super().__init__(name)
            self.add_component(FastAPIComponent, "fastapi_component")
            self.add_component(Subcomponent0, "subcomponent0")

    component0 = Component0("component0")

    async with component0:
        app = component0.components["subcomponent0"].app
        with TestClient(app) as client:
            response = client.get("/")
            assert response.json() == {"Hello": "World"}
