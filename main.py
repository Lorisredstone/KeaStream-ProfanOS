from dataclasses import dataclass
from typing import List

@dataclass
class Function:
    nb_args: int
    nb_return: int
    function: int # function pointer

@dataclass
class Element:
    data_type: int
    data_int: int
    data_str: str
    def __repr__(self):
        if self.data_type == 0:
            return f"int({self.data_int})"
        elif self.data_type == 1:
            return f"str(\"{self.data_str}\")"

@dataclass
class Pile:
    size_max: int
    elements: List[Element]
    size: int = 0

def add_pile(pile:Pile, element:Element) -> None:
    if pile.size == pile.size_max:
        print("Erreur, la pile esst trop grande")
        exit(1)
    pile.elements.append(element)
    pile.size += 1
    
def remove_pile(pile) -> Element:
    pile.size -= 1
    return pile.elements.pop()

@dataclass
class Instruction:
    name: str
    args: List[Element]
    
def add2int(pile:Pile) -> None:
    x = remove_pile(pile)
    y = remove_pile(pile)
    if x.data_type == 0 and y.data_type == 0:
        add_pile(pile, Element(0, x.data_int + y.data_int, ""))

def afficher(pile:Pile) -> None:
    x = remove_pile(pile)
    if x.data_type == 0:
        print(x.data_int)

buildins_names = [["add", "+"], ["print"]]
buildins_funcs = [Function(2, 1, add2int), Function(1, 0, afficher)]

def add_instruction(inst:str, liste_instructions:List[Instruction]) -> None:
    is_num = True
    liste_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(len(inst)):
        temp = False
        for j in range(len(liste_num)):
            if inst[i] == liste_num[j]:
                temp = True
        if not temp:
            is_num = False
    if is_num:
        liste_instructions.append(Instruction("addnb", [Element(0, int(inst), "")]))
    else:
        liste_instructions.append(Instruction("cmd", [Element(1, 0, inst)]))

def add_buffer(buffer1:str, liste_instructions:List[Instruction]) -> None:
    index = 0
    buffer2 = ""
    while index < len(buffer1):
        if buffer1[index] == ",":
            if len(buffer2) != 0:
                add_instruction(buffer2, liste_instructions)
                buffer2 = ""
        else:
            buffer2 += buffer1[index]
        index += 1
    add_instruction(buffer2, liste_instructions)

def compileall(code:str, liste_instructions:List[Instruction]) -> None:
    if code[len(code)-1] == ">":
        print("Erreur, on ne peut pas finir par >")
        exit(1)
    index = 0
    buffer = ""
    nb_fleches = 0
    while index < len(code):
        if code[index] == ">":
            if len(buffer) != 0:
                add_buffer(buffer, liste_instructions)
                buffer = ""
            nb_fleches += 1
            index += 1
            continue
        if nb_fleches != 0:
            liste_instructions.append(Instruction("fleche", [Element(0, nb_fleches, "")]))
            nb_fleches = 0
        buffer += code[index]
        index += 1
    add_buffer(buffer, liste_instructions)

def run(liste_instructions:List[Instruction]) -> None:
    stack = Pile(100, [])
    for i in range(len(liste_instructions)):
        inst:Instruction = liste_instructions[i]
        print(f"{inst.name + ' '*(10-len(inst.name))} : {inst}") # debug (HARDCODED AS HELL)
        print(f"stack : {stack.elements}") # debug
        if inst.name == "addnb":
            add_pile(stack, inst.args[0])
        elif inst.name == "cmd":
            for liste_id in range(len(buildins_names)):
                for element_id in range(len(buildins_names[liste_id])):
                    if inst.args[0].data_str == buildins_names[liste_id][element_id]:
                        if stack.size >= buildins_funcs[liste_id].nb_args:
                            buildins_funcs[liste_id].function(stack)
        elif inst.name == "fleche":
            pass

if __name__ == "__main__":
    code = """1,2,3,4>>>>+,+>+>print"""
    liste_instructions = []
    compileall(code, liste_instructions)
    run(liste_instructions)