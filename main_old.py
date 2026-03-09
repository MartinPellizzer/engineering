import pygame
import sys
import json

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ozone Engineering Assistant")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 36)

# --------- Project Data Skeleton ---------
project = {
    "client_name": "",
    "facility_name": "",
    "contact_person": "",
    "email": "",
    "phone": "",
    "location": "",
    "industry": ""
}
project["contaminants"] = []
project["target_concentrations"] = []
project["problem_definition"] = ""

design_basis = {

    "flow": {
        "average_m3h": 0,
        "max_m3h": 0
    },

    "contaminants": [
        {
            "name": "Iron",
            "current_mgL": 5,
            "target_mgL": 0.3,
            "removal_required": 0.94
        }
    ],

    "treatment_goals": [...],

    "infrastructure": {
        "power": "...",
        "oxygen": "...",
        "space": "...",
        "ventilation": "..."
    },

    "constraints": {
        "budget": "...",
        "deadline": "...",
        "regulatory": "...",
        "safety": "..."
    }
}

def save_project(filename="ozone_project.json"):

    data = {

        "project": project,
        "design_basis": design_basis,
        "workflow_status": workflow_status

    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("Project saved:", filename)

def load_project(filename="ozone_project.json"):

    global project
    global design_basis
    global workflow_status

    with open(filename, "r") as f:

        data = json.load(f)

        project = data["project"]
        design_basis = data["design_basis"]
        workflow_status = data["workflow_status"]

    print("Project loaded:", filename)

# --------- Input Box Helper Function ---------
def draw_input_box(x, y, w, h, active, text):
    color = BLUE if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h), 2)
    txt_surface = font.render(text, True, BLACK)
    screen.blit(txt_surface, (x+5, y+5))
    return pygame.Rect(x, y, w, h)

# --------- Button Helper Function ---------
def draw_button(text, x, y, w, h, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    txt = font.render(text, True, text_color)
    txt_rect = txt.get_rect(center=(x + w/2, y + h/2))
    screen.blit(txt, txt_rect)
    return pygame.Rect(x, y, w, h)

# --------- Main Input Screen ---------
def client_identification_screen():
    input_fields = ["client_name", "facility_name", "contact_person", "email", "phone", "location", "industry"]
    labels = ["Client Name:", "Facility Name:", "Contact Person:", "Email:", "Phone:", "Location:", "Industry:"]
    inputs = [""] * len(input_fields)
    active_index = 0
    warning_text = ""

    running = True
    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Display labels and input boxes
        input_boxes = []
        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (50, y_offset))
            box = draw_input_box(300, y_offset, 400, 40, i == active_index, inputs[i])
            input_boxes.append(box)
            y_offset += 70

        # Draw Next Button
        next_button = draw_button("Next", 300, y_offset + 20, 200, 50, BLUE, WHITE)

        # Display warning if any
        if warning_text:
            warning_surface = font.render(warning_text, True, RED)
            screen.blit(warning_surface, (50, y_offset + 90))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_index = i
                if next_button.collidepoint(event.pos):
                    if all(inp.strip() != "" for inp in inputs):
                        # Save inputs to project
                        for i, key in enumerate(input_fields):
                            project[key] = inputs[i].strip()
                        print("Client info saved:", project)
                        running = False  # Move to next step
                    else:
                        warning_text = "Please fill in all fields!"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_index] = inputs[active_index][:-1]
                elif event.key == pygame.K_TAB:
                    active_index = (active_index + 1) % len(inputs)
                else:
                    inputs[active_index] += event.unicode

def process_overview_screen():
    input_fields = ["process_description", "fluid_type", "treatment_stage"]
    labels = ["Process Description:", "Fluid Type:", "Treatment Stage:"]
    inputs = [""] * len(input_fields)
    active_index = 0
    warning_text = ""

    running = True
    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Display labels and input boxes
        input_boxes = []
        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (50, y_offset))
            box = draw_input_box(300, y_offset, 400, 40, i == active_index, inputs[i])
            input_boxes.append(box)
            y_offset += 70

        # Draw Next Button
        next_button = draw_button("Next", 300, y_offset + 20, 200, 50, BLUE, WHITE)

        # Display warning if any
        if warning_text:
            warning_surface = font.render(warning_text, True, RED)
            screen.blit(warning_surface, (50, y_offset + 90))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_index = i
                if next_button.collidepoint(event.pos):
                    if all(inp.strip() != "" for inp in inputs):
                        # Save inputs to project
                        for i, key in enumerate(input_fields):
                            project[key] = inputs[i].strip()
                        print("Process Overview saved:", {k: project[k] for k in input_fields})
                        running = False  # Move to next step
                    else:
                        warning_text = "Please fill in all fields!"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_index] = inputs[active_index][:-1]
                elif event.key == pygame.K_TAB:
                    active_index = (active_index + 1) % len(inputs)
                else:
                    inputs[active_index] += event.unicode

def flow_characteristics_screen():
    input_fields = ["average_flow", "max_flow", "flow_unit"]
    labels = ["Average Flow Rate:", "Maximum Flow Rate:", "Unit (m3/h or L/min):"]
    inputs = [""] * len(input_fields)
    active_index = 0
    warning_text = ""

    running = True
    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Display labels and input boxes
        input_boxes = []
        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (50, y_offset))
            box = draw_input_box(300, y_offset, 400, 40, i == active_index, inputs[i])
            input_boxes.append(box)
            y_offset += 70

        # Draw Next Button
        next_button = draw_button("Next", 300, y_offset + 20, 200, 50, BLUE, WHITE)

        # Display warning if any
        if warning_text:
            warning_surface = font.render(warning_text, True, RED)
            screen.blit(warning_surface, (50, y_offset + 90))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_index = i
                if next_button.collidepoint(event.pos):
                    try:
                        avg = float(inputs[0].strip())
                        maxf = float(inputs[1].strip())
                        unit = inputs[2].strip().lower()

                        if avg <= 0 or maxf <= 0:
                            warning_text = "Flow rates must be positive numbers."
                        elif maxf < avg:
                            warning_text = "Maximum flow must be ≥ average flow."
                        elif unit not in ["m3/h", "l/min"]:
                            warning_text = "Unit must be 'm3/h' or 'L/min'."
                        else:
                            # Convert to m3/h
                            if unit == "l/min":
                                avg = avg * 60 / 1000
                                maxf = maxf * 60 / 1000
                            project["average_flow"] = avg
                            project["max_flow"] = maxf
                            project["flow_unit"] = "m3/h"
                            print("Flow Characteristics saved:", {k: project[k] for k in ["average_flow","max_flow","flow_unit"]})
                            running = False
                    except ValueError:
                        warning_text = "Please enter valid numbers for flow rates."

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_index] = inputs[active_index][:-1]
                elif event.key == pygame.K_TAB:
                    active_index = (active_index + 1) % len(inputs)
                else:
                    inputs[active_index] += event.unicode

def contaminant_data_screen():
    inputs = ["", "", ""]  # name, current, target
    active_index = 0
    warning_text = ""
    running = True

    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Labels
        labels = ["Contaminant Name:", "Current Concentration (mg/L):", "Target Concentration (mg/L):"]
        input_boxes = []

        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (50, y_offset))
            box = draw_input_box(400, y_offset, 300, 40, i == active_index, inputs[i])
            input_boxes.append(box)
            y_offset += 70

        # Buttons
        add_button = draw_button("Add Contaminant", 150, y_offset + 20, 200, 50, BLUE, WHITE)
        next_button = draw_button("Next", 400, y_offset + 20, 200, 50, BLUE, WHITE)

        # Warning
        if warning_text:
            warning_surface = font.render(warning_text, True, (255,0,0))
            screen.blit(warning_surface, (50, y_offset + 90))

        # Display added contaminants
        y_list = y_offset + 150
        if project["contaminants"]:
            list_title = font.render("Added Contaminants:", True, BLACK)
            screen.blit(list_title, (50, y_list))
            y_list += 40
            for i, name in enumerate(project["contaminants"]):
                text = f"{name} | Current: {project['current_concentrations'][i]} | Target: {project['target_concentrations'][i]}"
                line = font.render(text, True, BLACK)
                screen.blit(line, (50, y_list))
                y_list += 30

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_index = i
                if add_button.collidepoint(event.pos):
                    try:
                        name = inputs[0].strip()
                        current = float(inputs[1].strip())
                        target = float(inputs[2].strip())

                        if name == "":
                            warning_text = "Contaminant name cannot be empty."
                        elif current <= 0 or target <= 0:
                            warning_text = "Concentrations must be positive numbers."
                        elif target >= current:
                            warning_text = "Target must be less than current concentration."
                        else:
                            if "current_concentrations" not in project:
                                project["current_concentrations"] = []
                            project["contaminants"].append(name)
                            project["current_concentrations"].append(current)
                            project["target_concentrations"].append(target)
                            inputs = ["", "", ""]
                            warning_text = ""
                            print("Contaminant added:", name, current, target)
                    except ValueError:
                        warning_text = "Current and target concentrations must be numbers."

                if next_button.collidepoint(event.pos):
                    if project["contaminants"]:
                        running = False
                    else:
                        warning_text = "Add at least one contaminant."
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_index] = inputs[active_index][:-1]
                elif event.key == pygame.K_TAB:
                    active_index = (active_index + 1) % len(inputs)
                else:
                    inputs[active_index] += event.unicode

def treatment_goals_screen():
    options = [
        "Oxidation of Metals",
        "Disinfection",
        "Color Removal",
        "Odor Removal",
        "Micropollutant Removal"
    ]
    selected = [False] * len(options)
    warning_text = ""
    running = True

    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Display options as checkbox-like buttons
        option_boxes = []
        for i, option in enumerate(options):
            color = BLUE if selected[i] else GRAY
            box = draw_button(option, 50, y_offset, 400, 50, color, WHITE)
            option_boxes.append(box)
            y_offset += 70

        # Draw Next Button
        next_button = draw_button("Next", 300, y_offset + 20, 200, 50, BLUE, WHITE)

        # Warning
        if warning_text:
            warning_surface = font.render(warning_text, True, (255,0,0))
            screen.blit(warning_surface, (50, y_offset + 90))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle option selection
                for i, box in enumerate(option_boxes):
                    if box.collidepoint(event.pos):
                        selected[i] = not selected[i]

                if next_button.collidepoint(event.pos):
                    if any(selected):
                        project["treatment_goals"] = [opt for i, opt in enumerate(options) if selected[i]]
                        print("Treatment Goals saved:", project["treatment_goals"])
                        running = False
                    else:
                        warning_text = "Select at least one treatment goal."

def infrastructure_screen():
    input_fields = ["available_power", "available_space", "existing_pumps", "oxygen_supply", "ventilation"]
    labels = ["Available Power:", "Available Space:", "Existing Pumps:", "Oxygen Supply:", "Ventilation:"]
    inputs = [""] * len(input_fields)
    active_index = 0
    warning_text = ""
    running = True

    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Display labels and input boxes
        input_boxes = []
        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (50, y_offset))
            box = draw_input_box(400, y_offset, 300, 40, i == active_index, inputs[i])
            input_boxes.append(box)
            y_offset += 70

        # Draw Next Button
        next_button = draw_button("Next", 300, y_offset + 20, 200, 50, BLUE, WHITE)

        # Display warning
        if warning_text:
            warning_surface = font.render(warning_text, True, (255,0,0))
            screen.blit(warning_surface, (50, y_offset + 90))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_index = i
                if next_button.collidepoint(event.pos):
                    if all(inp.strip() != "" for inp in inputs):
                        for i, key in enumerate(input_fields):
                            project[key] = inputs[i].strip()
                        print("Infrastructure saved:", {k: project[k] for k in input_fields})
                        running = False
                    else:
                        warning_text = "Please fill in all fields!"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_index] = inputs[active_index][:-1]
                elif event.key == pygame.K_TAB:
                    active_index = (active_index + 1) % len(inputs)
                else:
                    inputs[active_index] += event.unicode

def constraints_screen():
    input_fields = ["budget", "deadline", "regulatory_constraints", "safety_constraints"]
    labels = ["Budget:", "Deadline:", "Regulatory Constraints:", "Safety Constraints:"]
    inputs = [""] * len(input_fields)
    active_index = 0
    warning_text = ""
    running = True

    while running:
        screen.fill(WHITE)
        y_offset = 50

        # Display labels and input boxes
        input_boxes = []
        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (50, y_offset))
            box = draw_input_box(400, y_offset, 300, 40, i == active_index, inputs[i])
            input_boxes.append(box)
            y_offset += 70

        # Draw Finish Button
        finish_button = draw_button("Finish Step 2", 300, y_offset + 20, 200, 50, BLUE, WHITE)

        # Display warning
        if warning_text:
            warning_surface = font.render(warning_text, True, (255,0,0))
            screen.blit(warning_surface, (50, y_offset + 90))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_index = i
                if finish_button.collidepoint(event.pos):
                    if all(inp.strip() != "" for inp in inputs):
                        for i, key in enumerate(input_fields):
                            project[key] = inputs[i].strip()
                        print("Constraints saved:", {k: project[k] for k in input_fields})
                        running = False
                    else:
                        warning_text = "Please fill in all fields!"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_index] = inputs[active_index][:-1]
                elif event.key == pygame.K_TAB:
                    active_index = (active_index + 1) % len(inputs)
                else:
                    inputs[active_index] += event.unicode

def unit_standardization():

    # ----- Flow Conversion -----
    avg = project["average_flow"]
    maxf = project["max_flow"]
    unit = project["flow_unit"].lower()

    if unit == "m3/h":
        std_avg = avg
        std_max = maxf

    elif unit == "l/min":
        std_avg = avg * 0.06
        std_max = maxf * 0.06

    elif unit == "m3/day":
        std_avg = avg / 24
        std_max = maxf / 24

    else:
        print("Unknown flow unit. Cannot standardize.")
        return

    project["std_average_flow"] = std_avg
    project["std_max_flow"] = std_max
    project["std_flow_unit"] = "m3/h"


    # ----- Concentration Standardization -----

    project["std_current_concentrations"] = []
    project["std_target_concentrations"] = []

    for i in range(len(project["current_concentrations"])):

        current = project["current_concentrations"][i]
        target = project["target_concentrations"][i]

        # For now assume mg/L
        std_current = current
        std_target = target

        project["std_current_concentrations"].append(std_current)
        project["std_target_concentrations"].append(std_target)

    print("\nUnit Standardization Complete")

def unit_standardization_screen():

    unit_standardization()

    running = True

    while running:

        screen.fill(WHITE)

        title = font.render("Unit Standardization Summary", True, BLACK)
        screen.blit(title, (50,50))

        text1 = font.render(f"Average Flow: {project['std_average_flow']:.2f} m3/h", True, BLACK)
        screen.blit(text1,(50,150))

        text2 = font.render(f"Max Flow: {project['std_max_flow']:.2f} m3/h", True, BLACK)
        screen.blit(text2,(50,200))

        y = 260
        for i, contaminant in enumerate(project["contaminants"]):

            line = f"{contaminant}: {project['std_current_concentrations'][i]} -> {project['std_target_concentrations'][i]} mg/L"

            txt = font.render(line, True, BLACK)
            screen.blit(txt,(50,y))
            y += 40


        next_button = draw_button("Continue",300,500,200,50,BLUE,WHITE)

        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if next_button.collidepoint(event.pos):
                    running = False

def preliminary_engineering_checks():

    project["engineering_warnings"] = []
    project["engineering_notes"] = []

    # ---- Flow Check ----
    flow = project["std_average_flow"]

    if flow < 0.1:
        project["engineering_notes"].append(
            "Flow rate suggests lab or pilot scale system."
        )

    elif flow > 500:
        project["engineering_warnings"].append(
            "Very large flow rate. System may require multiple ozone generators."
        )

    # ---- Contaminant Treatability ----
    ozone_treatable = [
        "iron",
        "manganese",
        "hydrogen sulfide",
        "phenol",
        "cyanide",
        "color",
        "odor",
        "bacteria",
        "virus"
    ]

    for contaminant in project["contaminants"]:

        if contaminant.lower() not in ozone_treatable:

            project["engineering_notes"].append(
                f"Treatability of '{contaminant}' with ozone should be verified."
            )

    # ---- Removal Difficulty ----
    for i in range(len(project["contaminants"])):

        current = project["std_current_concentrations"][i]
        target = project["std_target_concentrations"][i]

        removal = (current - target) / current

        if removal > 0.9:

            project["engineering_warnings"].append(
                f"Very high removal required for {project['contaminants'][i]}."
            )

        elif removal > 0.7:

            project["engineering_notes"].append(
                f"High removal target for {project['contaminants'][i]}."
            )

    # ---- Infrastructure Check ----
    if project["oxygen_supply"] == "":
        project["engineering_warnings"].append(
            "Oxygen supply not specified."
        )

    if project["ventilation"] == "":
        project["engineering_notes"].append(
            "Ventilation requirements must be assessed for ozone safety."
        )

def engineering_checks_screen():

    preliminary_engineering_checks()

    running = True

    while running:

        screen.fill(WHITE)

        title = font.render("Preliminary Engineering Review", True, BLACK)
        screen.blit(title,(50,50))

        y = 150

        warning_title = font.render("Warnings:", True, BLACK)
        screen.blit(warning_title,(50,y))
        y += 40

        for w in project["engineering_warnings"]:

            txt = font.render(w,True,(200,0,0))
            screen.blit(txt,(50,y))
            y += 35


        y += 30

        notes_title = font.render("Engineering Notes:",True,BLACK)
        screen.blit(notes_title,(50,y))
        y += 40

        for n in project["engineering_notes"]:

            txt = font.render(n,True,BLACK)
            screen.blit(txt,(50,y))
            y += 35


        next_button = draw_button("Continue",300,500,200,50,BLUE,WHITE)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if next_button.collidepoint(event.pos):
                    running = False

def generate_problem_definition():

    lines = []

    lines.append("PROJECT PROBLEM DEFINITION\n")

    # ---- Client Info ----
    lines.append(f"Client: {project['client_name']}")
    lines.append(f"Facility: {project['facility_name']}")
    lines.append(f"Location: {project['location']}\n")

    # ---- Process Description ----
    lines.append("Process Description:")
    lines.append(project["process_description"] + "\n")

    # ---- Flow ----
    lines.append("Flow Characteristics:")
    lines.append(f"Average Flow: {project['std_average_flow']:.2f} m3/h")
    lines.append(f"Maximum Flow: {project['std_max_flow']:.2f} m3/h\n")

    # ---- Contaminants ----
    lines.append("Contaminants of Concern:")

    for i in range(len(project["contaminants"])):

        name = project["contaminants"][i]
        current = project["std_current_concentrations"][i]
        target = project["std_target_concentrations"][i]

        lines.append(f"{name}: {current} -> {target} mg/L")

    lines.append("")

    # ---- Treatment Goals ----
    lines.append("Treatment Objectives:")

    for goal in project["treatment_goals"]:
        lines.append(goal)

    lines.append("")

    # ---- Engineering Notes ----
    if project["engineering_notes"]:

        lines.append("Engineering Observations:")

        for n in project["engineering_notes"]:
            lines.append("- " + n)

        lines.append("")

    # ---- Engineering Warnings ----
    if project["engineering_warnings"]:

        lines.append("Engineering Warnings:")

        for w in project["engineering_warnings"]:
            lines.append("- " + w)

        lines.append("")

    project["problem_definition"] = "\n".join(lines)

def problem_definition_screen():

    generate_problem_definition()

    running = True

    while running:

        screen.fill(WHITE)

        title = font.render("Problem Definition Summary", True, BLACK)
        screen.blit(title,(50,50))

        y = 120

        lines = project["problem_definition"].split("\n")

        for line in lines:

            txt = font.render(line, True, BLACK)
            screen.blit(txt,(50,y))
            y += 30

            if y > 520:
                break

        next_button = draw_button("Continue",300,550,200,40,BLUE,WHITE)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if next_button.collidepoint(event.pos):
                    running = False

def generate_intake_report():

    lines = []

    lines.append("OZONE ENGINEERING CONSULTING REPORT")
    lines.append("Client Intake & Problem Definition\n")

    # Client Info
    lines.append("Client Information")
    lines.append("------------------")
    lines.append(f"Client: {project['client_name']}")
    lines.append(f"Facility: {project['facility_name']}")
    lines.append(f"Location: {project['location']}")
    lines.append(f"Contact: {project['contact_person']}")
    lines.append(f"Email: {project['email']}")
    lines.append(f"Phone: {project['phone']}\n")

    # Process
    lines.append("Process Overview")
    lines.append("----------------")
    lines.append(project["process_description"] + "\n")

    # Flow
    lines.append("Flow Characteristics")
    lines.append("--------------------")
    lines.append(f"Average Flow: {project['std_average_flow']:.2f} m3/h")
    lines.append(f"Maximum Flow: {project['std_max_flow']:.2f} m3/h\n")

    # Contaminants
    lines.append("Contaminants")
    lines.append("------------")

    for i in range(len(project["contaminants"])):

        name = project["contaminants"][i]
        current = project["std_current_concentrations"][i]
        target = project["std_target_concentrations"][i]

        lines.append(f"{name}: {current} -> {target} mg/L")

    lines.append("")

    # Goals
    lines.append("Treatment Objectives")
    lines.append("--------------------")

    for goal in project["treatment_goals"]:
        lines.append(goal)

    lines.append("")

    # Infrastructure
    lines.append("Infrastructure")
    lines.append("--------------")
    lines.append(f"Power: {project['available_power']}")
    lines.append(f"Space: {project['available_space']}")
    lines.append(f"Pumps: {project['existing_pumps']}")
    lines.append(f"Oxygen Supply: {project['oxygen_supply']}")
    lines.append(f"Ventilation: {project['ventilation']}\n")

    # Observations
    if project["engineering_notes"]:

        lines.append("Engineering Observations")
        lines.append("------------------------")

        for note in project["engineering_notes"]:
            lines.append("- " + note)

        lines.append("")

    # Warnings
    if project["engineering_warnings"]:

        lines.append("Engineering Warnings")
        lines.append("--------------------")

        for warn in project["engineering_warnings"]:
            lines.append("- " + warn)

        lines.append("")

    # Problem Definition
    lines.append("Problem Definition")
    lines.append("------------------")
    lines.append(project["problem_definition"])

    project["intake_report"] = "\n".join(lines)

def intake_report_screen():

    generate_intake_report()

    running = True

    while running:

        screen.fill(WHITE)

        title = font.render("Client Intake Report Preview", True, BLACK)
        screen.blit(title,(50,40))

        y = 100

        lines = project["intake_report"].split("\n")

        for line in lines:

            txt = font.render(line,True,BLACK)
            screen.blit(txt,(50,y))
            y += 28

            if y > 520:
                break

        save_button = draw_button("Save Report",200,540,180,40,BLUE,WHITE)
        next_button = draw_button("Continue",420,540,180,40,BLUE,WHITE)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if save_button.collidepoint(event.pos):

                    with open("client_intake_report.txt","w") as f:
                        f.write(project["intake_report"])

                    print("Report saved.")

                if next_button.collidepoint(event.pos):

                    running = False

def prepare_design_basis():

    global design_basis

    design_basis = {}

    # Flow
    design_basis["flow"] = {
        "average_m3h": project["std_average_flow"],
        "max_m3h": project["std_max_flow"]
    }

    # Contaminants
    contaminant_list = []

    for i in range(len(project["contaminants"])):

        name = project["contaminants"][i]
        current = project["std_current_concentrations"][i]
        target = project["std_target_concentrations"][i]

        removal = (current - target) / current

        contaminant_list.append({

            "name": name,
            "current_mgL": current,
            "target_mgL": target,
            "removal_required": removal

        })

    design_basis["contaminants"] = contaminant_list

    # Treatment goals
    design_basis["treatment_goals"] = project["treatment_goals"]

    # Infrastructure
    design_basis["infrastructure"] = {

        "power": project["available_power"],
        "oxygen": project["oxygen_supply"],
        "space": project["available_space"],
        "ventilation": project["ventilation"]

    }

    # Constraints
    design_basis["constraints"] = {

        "budget": project["budget"],
        "deadline": project["deadline"],
        "regulatory": project["regulatory_constraints"],
        "safety": project["safety_constraints"]

    }

    print("\nDesign Basis Prepared")

def design_basis_screen():

    prepare_design_basis()

    running = True

    while running:

        screen.fill(WHITE)

        title = font.render("Engineering Design Basis", True, BLACK)
        screen.blit(title,(50,50))

        y = 120

        flow_text = f"Flow: {design_basis['flow']['average_m3h']:.2f} m3/h (avg)"
        txt = font.render(flow_text,True,BLACK)
        screen.blit(txt,(50,y))
        y += 40

        txt = font.render("Contaminants:",True,BLACK)
        screen.blit(txt,(50,y))
        y += 40

        for c in design_basis["contaminants"]:

            line = f"{c['name']}  {c['current_mgL']} -> {c['target_mgL']} mg/L"
            txt = font.render(line,True,BLACK)
            screen.blit(txt,(50,y))
            y += 35

        y += 20

        txt = font.render("Treatment Goals:",True,BLACK)
        screen.blit(txt,(50,y))
        y += 40

        for g in design_basis["treatment_goals"]:

            txt = font.render(g,True,BLACK)
            screen.blit(txt,(50,y))
            y += 35

        next_button = draw_button("Start Site Assessment",250,520,300,40,BLUE,WHITE)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if next_button.collidepoint(event.pos):

                    running = False

def project_management_screen():

    running = True

    while running:

        screen.fill(WHITE)

        title = font.render("Project Management", True, BLACK)
        screen.blit(title,(50,50))

        save_button = draw_button("Save Project",300,200,200,50,BLUE,WHITE)
        load_button = draw_button("Load Project",300,300,200,50,BLUE,WHITE)
        continue_button = draw_button("Continue",300,400,200,50,BLUE,WHITE)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if save_button.collidepoint(event.pos):
                    save_project()

                if load_button.collidepoint(event.pos):
                    load_project()

                if continue_button.collidepoint(event.pos):
                    running = False
# --------- Main Loop ---------
def main():
    print("Welcome to Ozone Engineering Assistant")
    client_identification_screen()
    process_overview_screen()
    flow_characteristics_screen()
    contaminant_data_screen()
    treatment_goals_screen()
    infrastructure_screen()
    constraints_screen()

    unit_standardization_screen()
    
    engineering_checks_screen()
    problem_definition_screen()

    intake_report_screen()

    design_basis_screen()

    project_management_screen()

    print("\nStep 2 Complete! All client inputs collected.\n")
    print("Final Project Data:")
    for k, v in project.items():
        print(k, ":", v)

if __name__ == "__main__":
    main()
