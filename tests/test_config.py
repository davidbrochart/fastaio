from fastaio import Component, get_root_component, initialize


def test_config_override():
    class Subcomponent0(Component):
        def __init__(self, name, param0="param0", param1="param1"):
            super().__init__(name)
            self.param0 = param0
            self.param1 = param1
    
    class Subcomponent1(Component):
        def __init__(self, name, param0="param0"):
            super().__init__(name)
            self.param0 = param0

    class Subcomponent2(Component):
        def __init__(self, name, param2="param2"):
            super().__init__(name)
            self.add_component(Subcomponent3, "subcomponent3", param3="param3*")
            self.param2 = param2

    class Subcomponent3(Component):
        def __init__(self, name, param3="param3"):
            super().__init__(name)
            self.param3 = param3

    class Component0(Component):
        def __init__(self, name, param0="param0"):
            super().__init__(name)
            self.add_component(Subcomponent0, "subcomponent0", param0="param0*")
            self.add_component(Subcomponent1, "subcomponent1")
            self.add_component(Subcomponent2, "subcomponent2", param2="param2*")
            self.param0 = param0

    component0 = Component0("component0", param0="bar")
    initialize(component0)
    initialize(component0)
    assert component0.param0 == "bar"
    assert component0.components["subcomponent0"].param0 == "param0*"
    assert component0.components["subcomponent0"].param1 == "param1"
    assert component0.components["subcomponent1"].param0 == "param0"
    assert component0.components["subcomponent2"].param2 == "param2*"
    assert component0.components["subcomponent2"].components["subcomponent3"].param3 == "param3*"


def test_config_from_dict():
    class Subcomponent0(Component):
        def __init__(self, name, param0="param0", param1="param1"):
            super().__init__(name)
            self.param0 = param0
            self.param1 = param1
    
    class Subcomponent1(Component):
        def __init__(self, name, param0="param0"):
            super().__init__(name)
            self.param0 = param0

    class Subcomponent2(Component):
        def __init__(self, name, param2="param2"):
            super().__init__(name)
            self.add_component(Subcomponent3, "subcomponent3")
            self.param2 = param2

    class Subcomponent3(Component):
        def __init__(self, name, param3="param3"):
            super().__init__(name)
            self.param3 = param3

    class Component0(Component):
        def __init__(self, name, param0="param0"):
            super().__init__(name)
            self.add_component(Subcomponent0, "subcomponent0", param0="foo")
            self.add_component(Subcomponent1, "subcomponent1")
            self.add_component(Subcomponent2, "subcomponent2")
            self.param0 = param0

    config = {
        "component0": {
            "type": Component0,
            "config": {
                "param0": "bar",
            },
            "components": {
                "subcomponent0": {
                    "config": {
                        "param0": "foo2",
                    },
                },
                "subcomponent1": {
                    "config": {
                        "param0": "baz",
                    },
                },
                "subcomponent2": {
                    "config": {
                        "param2": "param2*",
                    },
                    "components": {
                        "subcomponent3": {
                            "config": {
                                "param3": "param3*",
                            },
                        },
                    },
                },
            },
        },
    }

    component0 = get_root_component(config)
    initialize(component0)
    assert component0.param0 == "bar"
    assert component0.components["subcomponent0"].param0 == "foo2"
    assert component0.components["subcomponent0"].param1 == "param1"
    assert component0.components["subcomponent1"].param0 == "baz"
    assert component0.components["subcomponent2"].param2 == "param2*"
    assert component0.components["subcomponent2"].components["subcomponent3"].param3 == "param3*"
