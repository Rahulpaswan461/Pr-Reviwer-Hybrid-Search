from tree_sitter import Language, Parser
import tree_sitter_javascript as ts_javascript

JS_LANGUAGE = Language(ts_javascript.language())
parser = Parser(JS_LANGUAGE)


def parse_javascript(file_path):
    with open(file_path, "rb") as file:
        source = file.read()

    tree = parser.parse(source)

    chunks = []

    def walk(node):
        if node.type in [
            "function_declaration",
            "method_definition",
            "class_declaration"
        ]:
            code = source[node.start_byte:node.end_byte].decode("utf-8")

            chunks.append({
                "file_path": file_path,
                "type": node.type,
                "name": node.child_by_field_name("name").text.decode("utf-8")
                    if node.child_by_field_name("name")
                    else None,
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "content": code
            })

        for child in node.children:
            walk(child)

    walk(tree.root_node)

    return chunks