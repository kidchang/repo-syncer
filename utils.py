import os
import jinja2

def render_jinja_templates(tpl_path, context, output_file):
    path, filename = os.path.split(tpl_path)
    result = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

    with open(output_file, 'wb') as of:
        of.write(result)
