from pathlib import Path
import re
from subprocess import call


def line_index_where(lines, predicate):
    found = [i for i, line in enumerate(lines) if predicate(line)]
    assert len(found) <= 1, found
    if found:
        return found[0]
    return -1


networktables_path = Path("utils/networktables.ini")

# assert 0 == call(f"scp -o ConnectTimeout=5 lvuser@10.55.28.2:/home/lvuser/networktables.ini {networktables_path.absolute()}")

assert networktables_path.exists()

properties_path = Path("properties.py")
assert properties_path.exists()

with open(networktables_path, "r") as f:
    networktables_lines = f.readlines()[1:]

with open(properties_path, "r") as f:
    all_properties_lines = f.readlines()

properties_start = 1 + line_index_where(all_properties_lines, lambda line: "class Properties" in line)
properties_end = line_index_where(all_properties_lines, lambda line: "values = " in line)
print(properties_start, properties_end)

# Validation

property_line_regex = re.compile(r'^\s*(\w+) = ntproperty\("\/Properties\/(\w+)",')

for line in all_properties_lines[properties_start:properties_end]:
    line = line.strip()
    if line:
        match = property_line_regex.match(line)
        if match:
            assert match[1] == match[2], f"{match[1]} is not {match[2]}"
        else:
            raise ValueError("Line does not match pattern :", line)

# Update

nt_double_line_pattern = re.compile(r'^double "\/Properties\/(\w+)"=([\d\.-]+)$')
nt_array_double_line_pattern = re.compile(r'^array double "\/Properties\/(\w+)"=([\d\.,-]+)$')

for line in networktables_lines:
    if line.startswith("double"):
        match = nt_double_line_pattern.match(line)
        assert match, "Line does not match nt_double_line_pattern " + line

        prop_name = match[1]
        value = match[2]
        assert float(value) is not None

        line_index = line_index_where(all_properties_lines, lambda line: (prop_name + " = ") in line)
        if line_index >= 0:
            assert properties_start <= line_index < properties_end

            line = all_properties_lines[line_index]
            new_line = re.sub(
                pattern=f'^(\\s*{prop_name} = ntproperty\\("/Properties/{prop_name}", )[\\d\\.-]+(, .+)',
                repl="\\g<1>" + str(value) + "\\g<2>",
                string=line
            )
            all_properties_lines[line_index] = new_line

    elif line.startswith("array double"):
        match = nt_array_double_line_pattern.match(line)
        assert match, "Line does not match nt_array_double_line_pattern " + line

        prop_name = match[1]
        value = match[2]

        line_index = line_index_where(all_properties_lines, lambda line: (prop_name + " = ") in line)
        if line_index >= 0:
            assert properties_start <= line_index < properties_end

            line = all_properties_lines[line_index]
            new_line = re.sub(
                pattern=f'^(\\s*{prop_name} = ntproperty\\("/Properties/{prop_name}", \\[)[\\d\\.,\s-]+(\\], .+)',
                repl="\\g<1>" + value.replace(", ", ",").replace(",", ", ") + "\\g<2>",
                string=line
            )
            all_properties_lines[line_index] = new_line
    else:
        raise Exception("Not supported nt property type :", line)


properties_path.unlink()
with open(properties_path, "w+") as f:
    f.writelines(all_properties_lines)
