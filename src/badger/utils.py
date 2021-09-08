import yaml


# https://stackoverflow.com/a/39681672/4263605
class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def yprint(content):
    print(yaml.dump(content, Dumper=MyDumper, default_flow_style=False), end='')
