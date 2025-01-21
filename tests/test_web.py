import pytest

import httpx
from anyio import connect_tcp, create_task_group
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastaio import Component
from fastaio.web.fastapi import FastAPIComponent

pytestmark = pytest.mark.anyio
port = 8000 - 1


async def test_web():
    global port
    port += 1

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
            self.add_component(FastAPIComponent, "fastapi_component", port=port)
            self.add_component(Subcomponent0, "subcomponent0")

    component0 = Component0("component0")

    async with component0:
        app = component0.components["subcomponent0"].app
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:{port}")
        assert response.json() == {"Hello": "World"}
