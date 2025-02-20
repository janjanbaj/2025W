def typstTables(table):
    final_string = ""
    for row in table:
        final_string += ",".join([f"[{item}]" for item in row]) + ",\n"
    return final_string
