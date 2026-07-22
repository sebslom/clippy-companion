import bpy
import gpu
import blf
import math
import time
import random
from gpu_extras.batch import batch_for_shader

bl_info = {
    "name": "Clippy Companion",
    "author": "Antigravity AI",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Clippy",
    "description": "An interactive 3D Viewport companion (like Clippy) that gives modeling tips and interactive tutorials.",
    "category": "Interface",
}

# --- GLOBAL DATA ---
TIPS = {
    "EN": [
        "Tip: Press Shift + A to add new objects, meshes, lights, or cameras!",
        "Tip: Press Tab to quickly toggle between Object Mode and Edit Mode.",
        "Tip: G is for Grab (move), R is for Rotate, and S is for Scale.",
        "Tip: While moving (G), rotating (R), or scaling (S), press X, Y, or Z to lock to that axis!",
        "Tip: Use the middle mouse button (scroll click) to orbit your 3D Viewport.",
        "Tip: Hold Shift + Middle Mouse Button to pan your view around the viewport.",
        "Tip: Press NumPad 0 to toggle active camera view.",
        "Tip: Press NumPad 1 for Front view, NumPad 3 for Right view, and NumPad 7 for Top view!",
        "Tip: In Edit Mode, press 1, 2, or 3 to switch selection modes (Vertex, Edge, Face).",
        "Tip: Press Ctrl + Z to undo, and Ctrl + Shift + Z to redo your actions.",
        "Tip: Press F2 to rename the selected object instantly.",
        "Tip: Press Alt + G, Alt + R, or Alt + S to reset an object's position, rotation, or scale!",
        "Tip: Press Shift + D to duplicate selected objects.",
        "Tip: In Edit Mode, select a face and press E to extrude it.",
        "Tip: Press Ctrl + B in Edit Mode to bevel selected edges or vertices.",
        "Tip: Press Ctrl + R in Edit Mode to add loop cuts to your mesh.",
        "Tip: Press I in Edit Mode to inset the selected faces.",
        "Tip: Hold Z to open the shading pie menu and switch between Wireframe, Solid, and Rendered modes!",
        "Tip: Press H to hide selected objects, and Alt + H to unhide everything in the scene!",
        "Tip: Press Slash (/) on NumPad to isolate selected objects in Local View!",
        "Tip: Press Ctrl + J to join multiple selected objects into a single mesh.",
        "Tip: Press P in Edit Mode to separate selected faces into a new object.",
        "Tip: Press M in Object Mode to move selected objects into a new Collection.",
        "Tip: Press Shift + Spacebar to open the full screen interactive tool menu!",
        "Tip: Press F3 to open the quick operator search bar to find any command!",
        "Tip: In Shader Editor, press Ctrl + T (with Node Wrangler enabled) to add Mapping and Texture Coordinate nodes!",
        "Tip: Press Spacebar to play or pause your keyframe animation!",
        "Tip: In Sculpt Mode, press Shift + F to adjust brush strength, and F to adjust brush size.",
        "Tip: Hold Shift while dragging any slider in Blender to make precision fine-adjustments!",
        "Tip: Hover over any input field and press Ctrl + C to copy its value, and Ctrl + V to paste it!"
    ],
    "PL": [
        "Wskazówka: Naciśnij Shift + A, aby dodać nowe obiekty, siatki, światła lub kamery!",
        "Wskazówka: Naciśnij Tab, aby szybko przełączać się między Trybem Obiektowym a Trybem Edycji.",
        "Wskazówka: G służy do przesuwania (Grab), R do obracania (Rotate), a S do skalowania (Scale).",
        "Wskazówka: Podczas przesuwania (G), obracania (R) lub skalowania (S) naciśnij X, Y lub Z, aby zablokować oś!",
        "Wskazówka: Użyj środkowego przycisku myszy (rolki), aby obracać widok 3D.",
        "Wskazówka: Przytrzymaj Shift + Środkowy Przycisk Myszy, aby przesuwać widok w boki.",
        "Wskazówka: Naciśnij NumPad 0, aby włączyć lub wyłączyć widok z aktywnej kamery.",
        "Wskazówka: NumPad 1 to widok z przodu, NumPad 3 to widok z prawej, a NumPad 7 to widok z góry!",
        "Wskazówka: W Trybie Edycji naciśnij 1, 2 lub 3, aby zmienić tryb zaznaczania (Wierzchołki, Krawędzie, Ściany).",
        "Wskazówka: Naciśnij Ctrl + Z, aby cofnąć, oraz Ctrl + Shift + Z, aby ponowić działanie.",
        "Wskazówka: Naciśnij F2, aby natychmiast zmienić nazwę zaznaczonego obiektu.",
        "Wskazówka: Naciśnij Alt + G, Alt + R lub Alt + S, aby zresetować pozycję, obrót lub skalę obiektu!",
        "Wskazówka: Naciśnij Shift + D, aby powielić (zduplikować) zaznaczone obiekty.",
        "Wskazówka: W Trybie Edycji zaznacz ścianę i naciśnij E, aby ją wyciągnąć (wytłoczyć).",
        "Wskazówka: Naciśnij Ctrl + B w Trybie Edycji, aby sfazować krawędzie lub wierzchołki.",
        "Wskazówka: Naciśnij Ctrl + R w Trybie Edycji, aby dodać cięcia pętli (Loop Cut).",
        "Wskazówka: Naciśnij I w Trybie Edycji, aby wciąć zaznaczoną ścianę (Inset).",
        "Wskazówka: Przytrzymaj Z, aby otworzyć menu trybów cieniowania (Wireframe, Solid, Rendered)!",
        "Wskazówka: Naciśnij H, aby ukryć zaznaczone obiekty, oraz Alt + H, aby odkryć wszystko!",
        "Wskazówka: Naciśnij Slash (/) na NumPadzie, aby odizolować zaznaczony obiekt w Widoku Lokalnym!",
        "Wskazówka: Naciśnij Ctrl + J, aby połączyć kilka zaznaczonych obiektów w jedną siatkę.",
        "Wskazówka: Naciśnij P w Trybie Edycji, aby odseparować zaznaczone ściany do nowego obiektu.",
        "Wskazówka: Naciśnij M w Trybie Obiektowym, aby przenieść zaznaczone obiekty do nowej Kolekcji.",
        "Wskazówka: Naciśnij Shift + Spacebar, aby otworzyć pełnoekranowe menu narzędzi!",
        "Wskazówka: Naciśnij F3, aby otworzyć szybkie wyszukiwanie operacji i poleceń!",
        "Wskazówka: W Edytorze Shaderów naciśnij Ctrl + T (z Node Wrangler), aby dodać węzły tekstury!",
        "Wskazówka: Naciśnij Spację, aby odtworzyć lub wstrzymać animację!",
        "Wskazówka: W Trybie Rzeźbienia naciśnij Shift + F dla siły pędzla, oraz F dla rozmiaru.",
        "Wskazówka: Przytrzymaj Shift podczas przeciągania suwaka, aby precyzyjnie dostosować wartość!",
        "Wskazówka: Najedź na dowolne pole numeryczne i naciśnij Ctrl + C, aby skopiować, oraz Ctrl + V, aby wkleić!"
    ]
}

# --- TUTORIAL DEFINITIONS ---
TUTORIALS = {
    "intro": {
        "title": {"EN": "Intro to Blender", "PL": "Wprowadzenie do Blendera"},
        "steps": [
            {
                "text": {
                    "EN": "Welcome to Blender! I am Clippy. Let's learn the basics. First, select the default Cube in the scene by left-clicking it.",
                    "PL": "Witaj w Blenderze! Jestem Clippy. Nauczmy się podstaw. Najpierw zaznacz domyślną Kostkę w scenie lewym przyciskiem myszy."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.name.startswith("Cube") and ctx.active_object.select_get()
            },
            {
                "text": {
                    "EN": "Great! Let's rename it to 'MyBox'. Press F2, type 'MyBox' and press Enter.",
                    "PL": "Świetnie! Zmieńmy jej nazwę na 'MyBox'. Naciśnij F2, wpisz 'MyBox' i naciśnij Enter."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.name == "MyBox"
            },
            {
                "text": {
                    "EN": "Excellent! Now let's enter Edit Mode to modify its geometry. Press Tab on your keyboard.",
                    "PL": "Doskonale! Wejdźmy w Tryb Edycji, aby zmodyfikować geometrię. Naciśnij Tab na klawiaturze."
                },
                "check": lambda ctx: ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Awesome! Let's change selection mode. Press '3' (top row, not Numpad) to switch to Face Selection mode.",
                    "PL": "Super! Zmieńmy tryb zaznaczania. Naciśnij klawisz '3' (górny rząd, nie NumPad), aby przejść do Zaznaczania Ścian."
                },
                "check": lambda ctx: ctx.tool_settings.mesh_select_mode[2] == True
            },
            {
                "text": {
                    "EN": "Superb! Let's go back to Object Mode. Press Tab again.",
                    "PL": "Wspaniale! Wróćmy do Trybu Obiektowego. Naciśnij ponownie klawisz Tab."
                },
                "check": lambda ctx: ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Congratulations! You completed the Blender Intro! Click Done to finish.",
                    "PL": "Gratulacje! Ukończyłeś Wprowadzenie do Blendera! Kliknij Gotowe, aby zakończyć."
                },
                "check": None
            }
        ]
    },
    "cushion": {
        "title": {"EN": "Modeling a Cushion", "PL": "Modelowanie Poduszki"},
        "steps": [
            {
                "text": {
                    "EN": "Let's model a cushion! First, delete the active object to clean up. Press X or Delete.",
                    "PL": "Zmodelujmy poduszkę! Najpierw usuń aktywny obiekt. Naciśnij X lub Delete."
                },
                "check": lambda ctx: ctx.active_object is None or ctx.active_object.name not in ctx.scene.objects
            },
            {
                "text": {
                    "EN": "Now add a Cylinder mesh. Press Shift+A, go to Mesh, and click Cylinder.",
                    "PL": "Teraz dodaj Walec. Naciśnij Shift+A, przejdź do Mesh i kliknij Cylinder."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH' and ctx.active_object.name.startswith("Cylinder")
            },
            {
                "text": {
                    "EN": "Let's flatten it. Press S, then Z, drag your mouse to scale it flat, and left-click to confirm.",
                    "PL": "Spłaszczmy go. Naciśnij S, potem Z, przesuń mysz, aby go spłaszczyć, i kliknij lewym przyciskiem."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.scale[2] < 0.25
            },
            {
                "text": {
                    "EN": "Perfect. Now enter Edit Mode. Press Tab.",
                    "PL": "Idealnie. Teraz wejdź w Tryb Edycji. Naciśnij Tab."
                },
                "check": lambda ctx: ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Let's round the edges. Press A to select everything. Then press Ctrl+B, move the mouse out, and scroll your wheel to add segments. Left-click to confirm.",
                    "PL": "Zaokrąglijmy krawędzie. Naciśnij A, aby zaznaczyć wszystko. Następnie Ctrl+B, przesuń mysz i użyj rolki, aby dodać podziały. Kliknij lewym."
                },
                "check": lambda ctx: ctx.active_object is not None and len(ctx.active_object.data.vertices) > 64
            },
            {
                "text": {
                    "EN": "Looking good! Let me return to Object Mode (Tab) and Shade Smooth. Right-click the cylinder and click Shade Smooth.",
                    "PL": "Wygląda świetnie! Wróć do Trybu Obiektowego (Tab), kliknij walec prawym i wybierz Shade Smooth."
                },
                "check": lambda ctx: ctx.mode == 'OBJECT' and ctx.active_object is not None and any(f.use_smooth for f in ctx.active_object.data.polygons)
            },
            {
                "text": {
                    "EN": "Fantastic work! You've modeled a smooth cushion base. Click Done to finish.",
                    "PL": "Fantastyczna robota! Zmodelowałeś bazę gładkiej poduszki. Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "lighting": {
        "title": {"EN": "Lighting & Camera", "PL": "Oświetlenie i Kamera"},
        "steps": [
            {
                "text": {
                    "EN": "Let's set up lighting! Add a Point Light to your scene. Press Shift+A -> Light -> Point Light.",
                    "PL": "Ustawmy oświetlenie! Dodaj światło punktowe. Naciśnij Shift+A -> Light -> Point."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'LIGHT'
            },
            {
                "text": {
                    "EN": "Great! Move the light higher above your scene. Press G, then Z, move your mouse upwards, and click.",
                    "PL": "Świetnie! Przesuń światło wyżej nad scenę. Naciśnij G, potem Z, przesuń mysz w górę i kliknij."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.location[2] > 2.5
            },
            {
                "text": {
                    "EN": "Now select the scene Camera. Click the camera object in the Viewport or Outliner.",
                    "PL": "Teraz zaznacz Kamerę sceny. Kliknij obiekt kamery w widoku lub w oknie Outliner."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'CAMERA'
            },
            {
                "text": {
                    "EN": "Let's snap the camera to your current 3D view. Position your view, then press Ctrl + Alt + NumPad 0!",
                    "PL": "Dopasujmy kamerę do obecnego widoku. Ustaw widok, a następnie naciśnij Ctrl + Alt + NumPad 0!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Awesome! You've mastered lighting and camera positioning! Click Done to finish.",
                    "PL": "Niesamowite! Opanowałeś pozycjonowanie światła i kamery! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "materials": {
        "title": {"EN": "Materials & Shading", "PL": "Materiały i Cieniowanie"},
        "steps": [
            {
                "text": {
                    "EN": "Let me show you how to color objects! First, select any Mesh object in your scene.",
                    "PL": "Pokażę Ci jak pokolorować obiekty! Najpierw zaznacz dowolną Siatkę (Mesh) w scenie."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Now open the Material Properties tab (red sphere icon) and click 'New' to add a material slot.",
                    "PL": "Otwórz zakładkę Właściwości Materiału (czerwona kulka) i kliknij 'New', aby dodać materiał."
                },
                "check": lambda ctx: ctx.active_object is not None and len(ctx.active_object.data.materials) > 0
            },
            {
                "text": {
                    "EN": "Let's view the material! Hold Z and select 'Material Preview' shading mode.",
                    "PL": "Zobaczmy materiał! Przytrzymaj Z i wybierz tryb 'Material Preview'."
                },
                "check": lambda ctx: hasattr(ctx.space_data, 'shading') and ctx.space_data.shading.type in {'MATERIAL', 'RENDERED'}
            },
            {
                "text": {
                    "EN": "Great! Now click 'Base Color' in Material Properties and pick your favorite color!",
                    "PL": "Super! Kliknij 'Base Color' we właściwościach materiału i wybierz swój ulubiony kolor!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Beautiful! You now know how to apply materials and preview shaders! Click Done to finish.",
                    "PL": "Pięknie! Wiesz już jak nakładać materiały i podglądać shadery! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "extrude": {
        "title": {"EN": "Inset & Extrude", "PL": "Wcinanie i Wytłaczanie"},
        "steps": [
            {
                "text": {
                    "EN": "Let me teach you Inset and Extrude! Select a Mesh object and press Tab to enter Edit Mode.",
                    "PL": "Nauczę Cię operacji Inset i Extrude! Zaznacz Siatkę i naciśnij Tab, aby wejść w Tryb Edycji."
                },
                "check": lambda ctx: ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Switch to Face Selection mode by pressing key '3' (top number row).",
                    "PL": "Przełącz na Zaznaczanie Ścian wciskając klawisz '3' (górny rząd cyfr)."
                },
                "check": lambda ctx: ctx.tool_settings.mesh_select_mode[2] == True
            },
            {
                "text": {
                    "EN": "Select any face on your object, then press 'I' to Inset the face inward, then left-click.",
                    "PL": "Zaznacz dowolną ścianę obiektu, naciśnij 'I', aby wciąć ścianę do środka, i kliknij lewym."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "With that face selected, press 'E' to Extrude it outwards or inwards, then left-click to place.",
                    "PL": "Mając zaznaczoną ścianę, naciśnij 'E', aby ją wyciągnąć (wytłoczyć) i kliknij lewym."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Tab to return to Object Mode.",
                    "PL": "Naciśnij Tab, aby wrócić do Trybu Obiektowego."
                },
                "check": lambda ctx: ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Masterclass complete! Inset (I) and Extrude (E) are essential modeling tools! Click Done to finish.",
                    "PL": "Lekcja zakończona! Inset (I) oraz Extrude (E) to podstawowe narzędzia modelowania! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "sculpting": {
        "title": {"EN": "Sculpting Basics", "PL": "Podstawy Rzeźbienia"},
        "steps": [
            {
                "text": {
                    "EN": "Let's sculpt! Select a Mesh object and switch to Sculpt Mode (top left mode menu).",
                    "PL": "Rzeźbijmy! Zaznacz Siatkę i przejdź do Trybu Rzeźbienia (Sculpt Mode w lewym górnym menu)."
                },
                "check": lambda ctx: ctx.mode == 'SCULPT'
            },
            {
                "text": {
                    "EN": "Press 'F' to adjust the sculpting brush size, move mouse and click to confirm.",
                    "PL": "Naciśnij 'F', aby zmienić rozmiar pędzla rzeźbiarskiego, przesuń mysz i kliknij."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Shift+'F' to adjust brush strength, move mouse and click.",
                    "PL": "Naciśnij Shift+'F', aby dostosować siłę pędzla, przesuń mysz i kliknij."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Click and drag across the mesh surface to sculpt 3D detail!",
                    "PL": "Kliknij i przeciągnij po powierzchni siatki, aby rzeźbić detale 3D!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Switch mode back to Object Mode.",
                    "PL": "Przełącz tryb z powrotem na Tryb Obiektowy."
                },
                "check": lambda ctx: ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Awesome! Sculpting lets you craft organic 3D shapes freely! Click Done to finish.",
                    "PL": "Niesamowite! Rzeźbienie pozwala swobodnie tworzyć organiczne kształty! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "modifiers": {
        "title": {"EN": "Subdivision Surface", "PL": "Modyfikator Subdivision"},
        "steps": [
            {
                "text": {
                    "EN": "Let's learn Modifiers! Select any Mesh object in Object Mode.",
                    "PL": "Poznajmy Modyfikatory! Zaznacz dowolną Siatkę w Trybie Obiektowym."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Modifier Properties (blue wrench icon) and click Add Modifier.",
                    "PL": "Otwórz Właściwości Modyfikatorów (niebieski klucz) i kliknij Dodaj Modyfikator."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Add a Subdivision Surface modifier (or shortcut Ctrl+2).",
                    "PL": "Dodaj modyfikator Subdivision Surface (lub użyj skrótu Ctrl+2)."
                },
                "check": lambda ctx: ctx.active_object is not None and any(m.type == 'SUBSURF' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Notice how smooth your mesh becomes! Increase Viewport Levels to 2.",
                    "PL": "Zobacz jak gładki staje się obiekt! Zwiększ poziom podziału (Viewport Levels) do 2."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Subdivision Surface non-destructively smoothes 3D geometry! Click Done to finish.",
                    "PL": "Subdivision Surface elastycznie wygładza geometrię 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "animation": {
        "title": {"EN": "Keyframe Animation", "PL": "Animacja Kluczowa"},
        "steps": [
            {
                "text": {
                    "EN": "Let me teach you Keyframe Animation! Select an object and ensure Timeline playhead is at frame 1.",
                    "PL": "Nauczę Cię Animacji Kluczowej! Zaznacz obiekt i upewnij się, że czas jest na klatce 1."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.scene.frame_current == 1
            },
            {
                "text": {
                    "EN": "Press 'I' in 3D Viewport to open Insert Keyframe menu, and click Location.",
                    "PL": "Naciśnij 'I' w widoku 3D, aby otworzyć menu klatek kluczowych i wybierz Location (Położenie)."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.animation_data is not None
            },
            {
                "text": {
                    "EN": "Drag your Timeline slider at bottom to frame 40.",
                    "PL": "Przesuń suwak osi czasu na dole do klatki 40."
                },
                "check": lambda ctx: ctx.scene.frame_current >= 30
            },
            {
                "text": {
                    "EN": "Move your object to a new location (G), then press 'I' and select Location again!",
                    "PL": "Przesuń obiekt w nowe miejsce (G), a następnie naciśnij 'I' i wybierz ponownie Location!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Spacebar to play your keyframe animation!",
                    "PL": "Naciśnij Spację, aby odtworzyć utworzoną animację!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Fantastic! You've animated your first 3D object in Blender! Click Done to finish.",
                    "PL": "Fantastycznie! Zaanimowałeś swój pierwszy obiekt 3D w Blenderze! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "uv_unwrap": {
        "title": {"EN": "UV Unwrapping", "PL": "Rozwijanie UV"},
        "steps": [
            {
                "text": {
                    "EN": "Let's learn UV Unwrapping! Select a Mesh object and enter Edit Mode (Tab).",
                    "PL": "Nauczmy się Rozwijania UV! Zaznacz Siatkę i wejdź w Tryb Edycji (Tab)."
                },
                "check": lambda ctx: ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Press 'A' to select all vertices and faces.",
                    "PL": "Naciśnij 'A', aby zaznaczyć wszystkie wierzchołki i ściany."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press 'U' to open the UV Mapping menu.",
                    "PL": "Naciśnij 'U', aby otworzyć menu Mapowania UV."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Click 'Smart UV Project' and press OK to auto-unwrap your mesh.",
                    "PL": "Kliknij 'Smart UV Project' i naciśnij OK, aby automatycznie rozwinąć siatkę."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Tab to return to Object Mode.",
                    "PL": "Naciśnij Tab, aby wrócić do Trybu Obiektowego."
                },
                "check": lambda ctx: ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Great job! UV unwrapping projects 2D textures onto 3D surfaces! Click Done to finish.",
                    "PL": "Świetna robota! Rozwijanie UV pozwala nakładać tekstury 2D na obiekty 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "nodes": {
        "title": {"EN": "Shader Nodes", "PL": "Węzły Shadera"},
        "steps": [
            {
                "text": {
                    "EN": "Let me show you Shader Nodes! Switch to the Shading workspace tab at top.",
                    "PL": "Pokażę Ci Węzły Shadera! Przełącz się na zakładkę Shading na samej górze."
                },
                "check": lambda ctx: ctx.workspace.name == 'Shading' or (hasattr(ctx.space_data, 'tree_type') and ctx.space_data.tree_type == 'ShaderNodeTree')
            },
            {
                "text": {
                    "EN": "Select your object and click 'New' in the Shader Editor panel.",
                    "PL": "Zaznacz obiekt i kliknij 'New' w panelu Edytora Shaderów."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.active_material is not None
            },
            {
                "text": {
                    "EN": "Inside Shader Editor, press Shift+A -> Texture -> Noise Texture to add a noise node.",
                    "PL": "W Edytorze Shaderów naciśnij Shift+A -> Texture -> Noise Texture, aby dodać węzeł szumu."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Connect Color output of Noise Texture to Base Color of Principled BSDF.",
                    "PL": "Połącz wyjście Color z Noise Texture z wejściem Base Color węzła Principled BSDF."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Hold Z and switch to Material Preview to see your procedural texture pattern!",
                    "PL": "Przytrzymaj Z i przełącz na Podgląd Materiału, aby zobaczyć proceduralny wzór!"
                },
                "check": lambda ctx: hasattr(ctx.space_data, 'shading') and ctx.space_data.shading.type in {'MATERIAL', 'RENDERED'}
            },
            {
                "text": {
                    "EN": "Masterclass complete! Shader nodes unlock unlimited materials! Click Done to finish.",
                    "PL": "Lekcja zakończona! Węzły shadera dają nieograniczone możliwości! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "cloth": {
        "title": {"EN": "Cloth Simulation", "PL": "Symulacja Tkaniny"},
        "steps": [
            {
                "text": {
                    "EN": "Let's create a cloth simulation! First, add a Grid mesh to your scene. Press Shift+A -> Mesh -> Grid.",
                    "PL": "Stwórzmy symulację tkaniny! Najpierw dodaj siatkę Grid. Naciśnij Shift+A -> Mesh -> Grid."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH' and ctx.active_object.name.startswith("Grid")
            },
            {
                "text": {
                    "EN": "Move the grid higher above your scene floor. Press G, then Z, move upwards and click.",
                    "PL": "Przesuń siatkę wyżej nad podłogę sceny. Naciśnij G, potem Z, przesuń w górę i kliknij."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.location[2] > 2.0
            },
            {
                "text": {
                    "EN": "Open Physics Properties (blue orbital atom icon on right panel) and click 'Cloth'.",
                    "PL": "Otwórz Właściwości Fizyki (niebieski atom po prawej) i kliknij 'Cloth' (Tkanina)."
                },
                "check": lambda ctx: ctx.active_object is not None and any(m.type == 'CLOTH' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Press Spacebar to play the physics animation and watch your cloth drop and drape!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację fizyki i zobaczyć jak tkanina opada!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Awesome! You've created a dynamic 3D cloth simulation! Click Done to finish.",
                    "PL": "Niesamowite! Stworzyłeś dynamiczną symulację tkaniny 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "particles": {
        "title": {"EN": "Particle System", "PL": "System Cząsteczek"},
        "steps": [
            {
                "text": {
                    "EN": "Let's create a particle emitter! Select any Mesh object in your scene.",
                    "PL": "Stwórzmy emiter cząsteczek! Zaznacz dowolną Siatkę (Mesh) w scenie."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Particle Properties (three connected dots icon) and click '+' to add a Particle System.",
                    "PL": "Otwórz Właściwości Cząsteczek (trzy połączone kropki) i kliknij '+', aby dodać system."
                },
                "check": lambda ctx: ctx.active_object is not None and len(ctx.active_object.particle_systems) > 0
            },
            {
                "text": {
                    "EN": "Press Spacebar to play animation and see particles bursting out from your object!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację i zobaczyć tryskające cząsteczki!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Spectacular! Particle systems are used for sparks, rain, smoke, and hair! Click Done to finish.",
                    "PL": "Widowiskowe! Systemy cząsteczek tworzą deszcz, iskry, dym i włosy! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "grease_pencil": {
        "title": {"EN": "2D Grease Pencil", "PL": "2D Grease Pencil"},
        "steps": [
            {
                "text": {
                    "EN": "Let's draw 2D art in 3D! Add a Blank Grease Pencil object. Press Shift+A -> Grease Pencil -> Blank.",
                    "PL": "Rysujmy 2D w 3D! Dodaj pusty obiekt Grease Pencil. Naciśnij Shift+A -> Grease Pencil -> Blank."
                },
                "check": lambda ctx: ctx.active_object is not None and (ctx.active_object.type == 'GPENCIL' or ctx.active_object.type == 'GREASEPENCIL')
            },
            {
                "text": {
                    "EN": "Switch to Draw Mode using the top-left mode dropdown menu.",
                    "PL": "Przełącz się na Tryb Rysowania (Draw Mode) w lewym górnym menu."
                },
                "check": lambda ctx: 'DRAW' in ctx.mode
            },
            {
                "text": {
                    "EN": "Click and drag across the 3D Viewport to draw 2D strokes in 3D space!",
                    "PL": "Kliknij i przeciągnij po widoku 3D, aby rysować pociągnięcia 2D w przestrzeni 3D!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Switch mode back to Object Mode.",
                    "PL": "Przełącz tryb z powrotem na Tryb Obiektowy."
                },
                "check": lambda ctx: ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Wonderful! Grease Pencil blends 2D animation directly inside 3D space! Click Done to finish.",
                    "PL": "Wspaniale! Grease Pencil łączy animację 2D z przestrzenią 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "rigid_body": {
        "title": {"EN": "Rigid Body Physics", "PL": "Ciała Sztywne (Rigid Body)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's make objects tumble with gravity! Select any Cube or Mesh in your scene.",
                    "PL": "Sprawmy, by obiekty spadały z grawitacją! Zaznacz dowolną Kostkę lub Siatkę."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Physics Properties (blue atom icon) and click 'Rigid Body'.",
                    "PL": "Otwórz Właściwości Fizyki (niebieski atom) i kliknij 'Rigid Body' (Ciało Sztywne)."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.rigid_body is not None
            },
            {
                "text": {
                    "EN": "Press Spacebar to play animation and watch your object fall with physical gravity!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację i zobaczyć jak obiekt spada z grawitacją!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Great job! Rigid Body physics powers realistic collisions and destructions! Click Done to finish.",
                    "PL": "Świetna robota! Fizyka Rigid Body tworzy realistyczne zderzenia i zniszczenia! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "bevel_modifier": {
        "title": {"EN": "Bevel Modifier", "PL": "Modyfikator Bevel"},
        "steps": [
            {
                "text": {
                    "EN": "Let's round mesh edges non-destructively! Select a Cube mesh in Object Mode.",
                    "PL": "Zaokrąglijmy krawędzie siatki elastycznie! Zaznacz Kostkę w Trybie Obiektowym."
                },
                "check": lambda ctx: ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Modifier Properties (blue wrench icon) and click Add Modifier -> Bevel.",
                    "PL": "Otwórz Właściwości Modyfikatorów (niebieski klucz) i dodaj modyfikator Bevel (Faza)."
                },
                "check": lambda ctx: ctx.active_object is not None and any(m.type == 'BEVEL' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Increase the Segments slider to 3 or 4 to catch smooth realistic highlights on edges!",
                    "PL": "Zwiększ suwak Segments do 3 lub 4, aby uzyskać gładkie, realistyczne odblaski na krawędziach!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Excellent! Hard edges don't exist in nature—always use Bevel for realism! Click Done to finish.",
                    "PL": "Doskonale! Ostre krawędzie nie istnieją w naturze—zawsze używaj Bevel dla realizmu! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    }
}

# --- PROCEDURAL DRAWING HELPERS ---
def draw_polyline(points, color, width, viewport_size):
    if len(points) < 2:
        return
    gpu.state.blend_set('ALPHA')
    shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": points})
    shader.bind()
    shader.uniform_float("color", color)
    shader.uniform_float("viewportSize", viewport_size)
    shader.uniform_float("lineWidth", width)
    batch.draw(shader)

def get_uniform_color_shader():
    try:
        return gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    except Exception:
        return gpu.shader.from_builtin('UNIFORM_COLOR')

def draw_rect(x, y, w, h, color):
    gpu.state.blend_set('ALPHA')
    shader = get_uniform_color_shader()
    coords = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    batch = batch_for_shader(shader, 'TRI_STRIP', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_rect_outline(x, y, w, h, color, width, viewport_size):
    coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    draw_polyline(coords, color, width, viewport_size)

def draw_circle(cx, cy, r, color, segments=24):
    gpu.state.blend_set('ALPHA')
    shader = get_uniform_color_shader()
    coords = [(cx, cy)]
    for i in range(segments + 1):
        angle = (i / segments) * (2.0 * math.pi)
        coords.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_circle_outline(cx, cy, r, color, width, viewport_size, segments=24):
    coords = []
    for i in range(segments + 1):
        angle = (i / segments) * (2.0 * math.pi)
        coords.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw_polyline(coords, color, width, viewport_size)

def draw_rounded_rect(x, y, w, h, r, color, segments=8):
    gpu.state.blend_set('ALPHA')
    shader = get_uniform_color_shader()
    r = min(r, w / 2.0, h / 2.0)
    cx, cy = x + w / 2.0, y + h / 2.0
    coords = [(cx, cy)]
    
    def add_arc(acx, acy, start_angle, end_angle):
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / segments)
            coords.append((acx + math.cos(angle) * r, acy + math.sin(angle) * r))
            
    add_arc(x + w - r, y + r, 1.5 * math.pi, 2.0 * math.pi)
    add_arc(x + w - r, y + h - r, 0.0, 0.5 * math.pi)
    add_arc(x + r, y + h - r, 0.5 * math.pi, math.pi)
    add_arc(x + r, y + r, math.pi, 1.5 * math.pi)
    coords.append(coords[1])
    
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_rounded_rect_outline(x, y, w, h, r, color, width, viewport_size, segments=8):
    r = min(r, w / 2.0, h / 2.0)
    coords = []
    
    def add_arc(acx, acy, start_angle, end_angle):
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / segments)
            coords.append((acx + math.cos(angle) * r, acy + math.sin(angle) * r))
            
    add_arc(x + w - r, y + r, 1.5 * math.pi, 2.0 * math.pi)
    add_arc(x + w - r, y + h - r, 0.0, 0.5 * math.pi)
    add_arc(x + r, y + h - r, 0.5 * math.pi, math.pi)
    add_arc(x + r, y + r, math.pi, 1.5 * math.pi)
    coords.append(coords[0])
    
    draw_polyline(coords, color, width, viewport_size)

def draw_bubble_pointer(bx, by, px, py, is_left, bw, color, border_color, border_width, viewport_size):
    gpu.state.blend_set('ALPHA')
    if is_left:
        p1 = (px, py)
        p2 = (bx + bw, by + 12)
        p3 = (bx + bw, by + 26)
    else:
        p1 = (px, py)
        p2 = (bx, by + 12)
        p3 = (bx, by + 26)
        
    shader = get_uniform_color_shader()
    batch = batch_for_shader(shader, 'TRIS', {"pos": [p1, p2, p3]})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)
    
    draw_polyline([p2, p1, p3], border_color, border_width, viewport_size)

# --- TEXT WRAPPING ---
def wrap_text(text, max_width, font_id=0, font_size=14):
    blf.size(font_id, font_size)
    paragraphs = text.split('\n')
    lines = []
    for para in paragraphs:
        if not para:
            lines.append("")
            continue
        words = para.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word]) if current_line else word
            w, h = blf.dimensions(font_id, test_line)
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))
    return lines

# --- GEOMETRY GENERATOR ---
def get_paperclip_path(cx, cy, s):
    points = []
    
    def add_arc(acx, acy, r, start, end, steps=12):
        for i in range(steps + 1):
            a = start + (end - start) * (i / steps)
            points.append((acx + math.cos(a) * r, acy + math.sin(a) * r))

    points.append((cx + 4*s, cy + 10*s))
    points.append((cx + 4*s, cy - 10*s))
    add_arc(cx, cy - 10*s, 4*s, 0.0, -math.pi, steps=10)
    points.append((cx - 4*s, cy + 22*s))
    add_arc(cx + 4*s, cy + 22*s, 8*s, math.pi, 0.0, steps=10)
    points.append((cx + 12*s, cy - 25*s))
    add_arc(cx, cy - 25*s, 12*s, 0.0, -math.pi, steps=10)
    points.append((cx - 12*s, cy + 5*s))
    
    return points

def rotate_points(points, cx, cy, angle):
    if angle == 0.0:
        return points
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rotated = []
    for px, py in points:
        dx = px - cx
        dy = py - cy
        rx = cx + dx * cos_a - dy * sin_a
        ry = cy + dx * sin_a + dy * cos_a
        rotated.append((rx, ry))
    return rotated

# --- CLIPPY STATE ---
class ClippyState:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.viewport_size = (100, 100)
        self.mouse_pos = (0, 0)
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.click_start_time = 0.0
        self.click_start_pos = (0, 0)
        
        # Animations
        self.blink_timer = 0.0
        self.is_blinking = False
        self.blink_duration = 0.16
        self.next_blink_time = time.time() + random.uniform(3.0, 6.0)
        self.blink_end_time = 0.0
        
        self.nod_start_time = 0.0
        self.jump_start_time = 0.0
        self.rotation = 0.0
        
        # Talking & Expression
        self.expression = 'HAPPY'
        self.is_talking = False
        
        # Speech Bubble
        self.bubble_visible = False
        self.bubble_text_target = ""
        self.bubble_char_count = 0
        self.bubble_lines = []
        self.last_char_time = 0.0
        self.bubble_buttons = []
        
        # Context Menu
        self.menu_visible = False
        self.menu_x = 0
        self.menu_y = 0
        self.menu_items = []
        self.menu_hover_idx = -1
        self.menu_scroll_offset = 0
        self.language = 'EN'
        
        # Tutorial State
        self.active_tutorial = None
        self.tutorial_step_idx = 0

# --- VIEWPORT DRAW CALLBACK ---
def draw_callback(op, context):
    state = op.state
    # Update viewport size to match region dimensions
    state.viewport_size = (context.region.width, context.region.height)
    s = 1.5 # Scale factor
    
    # --- ANIMATION UPDATES (Running in draw thread) ---
    now = time.time()
    
    # 1. Typing bubble effect
    if state.bubble_visible and state.bubble_text_target:
        if state.bubble_char_count < len(state.bubble_text_target):
            if now - state.last_char_time > 0.015:
                # Add characters depending on time elapsed
                chars_to_add = int((now - state.last_char_time) / 0.015)
                if chars_to_add > 0:
                    state.bubble_char_count = min(state.bubble_char_count + chars_to_add, len(state.bubble_text_target))
                    state.last_char_time = now
                state.is_talking = True
        else:
            if state.is_talking:
                state.is_talking = False
                
    # 2. Blinking eye effect
    if now > state.next_blink_time:
        state.is_blinking = True
        state.next_blink_time = now + random.uniform(3.5, 6.5)
        state.blink_end_time = now + state.blink_duration
    if state.is_blinking and now > state.blink_end_time:
        state.is_blinking = False
        
    # 3. Real-time state check for tutorials
    if state.active_tutorial and not state.is_talking:
        step = state.active_tutorial['steps'][state.tutorial_step_idx]
        check_func = step.get('check')
        if check_func:
            try:
                if check_func(context):
                    op.next_tutorial_step()
            except Exception:
                pass
                
    # Calculate animations offsets
    breath_offset = 1.5 * math.sin(time.time() * 2.0) * s
    nod_offset = 0.0
    jump_offset = 0.0
    
    if state.nod_start_time > 0.0:
        t = time.time() - state.nod_start_time
        if t < 0.4:
            nod_offset = 6.0 * math.sin(t * 30.0) * s
        else:
            state.nod_start_time = 0.0
            
    if state.jump_start_time > 0.0:
        t = time.time() - state.jump_start_time
        duration = 0.6
        if t < duration:
            progress = t / duration
            jump_offset = 30.0 * math.sin(progress * math.pi) * s
            state.rotation = progress * 2.0 * math.pi
        else:
            state.jump_start_time = 0.0
            state.rotation = 0.0
            
    dcx = state.x
    dcy = state.y + breath_offset + nod_offset + jump_offset
    
    # 1. Shadow of paperclip body
    shadow_points = get_paperclip_path(dcx + 2*s, dcy - 2*s, s)
    shadow_points = rotate_points(shadow_points, dcx, dcy, state.rotation)
    draw_polyline(shadow_points, (0.0, 0.0, 0.0, 0.22), 8.0*s, state.viewport_size)
    
    # 2. Border of paperclip body
    border_points = get_paperclip_path(dcx, dcy, s)
    border_points = rotate_points(border_points, dcx, dcy, state.rotation)
    draw_polyline(border_points, (0.2, 0.2, 0.23, 1.0), 6.5*s, state.viewport_size)
    
    # 3. Main paperclip body (metallic silver)
    draw_polyline(border_points, (0.83, 0.84, 0.86, 1.0), 4.0*s, state.viewport_size)
    # Subtly lighter inner highlights
    draw_polyline(border_points, (0.95, 0.95, 0.97, 1.0), 1.2*s, state.viewport_size)
    
    # 4. Eyes & Pupils
    # Calculate eye centers
    lex_orig, ley_orig = dcx - 7.5*s, dcy + 13*s
    rex_orig, rey_orig = dcx + 7.5*s, dcy + 13*s
    
    rotated_eyes = rotate_points([(lex_orig, ley_orig), (rex_orig, rey_orig)], dcx, dcy, state.rotation)
    lex, ley = rotated_eyes[0]
    rex, rey = rotated_eyes[1]
    
    eye_r = 7.0*s
    
    if state.is_blinking:
        # Drawing eyelids closed
        lid_y_l = ley - 1*s
        lid_y_r = rey - 1*s
        draw_polyline([(lex - 6*s, lid_y_l + 1*s), (lex, lid_y_l - 1*s), (lex + 6*s, lid_y_l + 1*s)], (0.1, 0.1, 0.1, 1.0), 2.5*s, state.viewport_size)
        draw_polyline([(rex - 6*s, lid_y_r + 1*s), (rex, lid_y_r - 1*s), (rex + 6*s, lid_y_r + 1*s)], (0.1, 0.1, 0.1, 1.0), 2.5*s, state.viewport_size)
    else:
        # Draw white sclera
        draw_circle(lex, ley, eye_r, (1.0, 1.0, 1.0, 1.0))
        draw_circle(rex, rey, eye_r, (1.0, 1.0, 1.0, 1.0))
        
        # Border
        draw_circle_outline(lex, ley, eye_r, (0.1, 0.1, 0.1, 1.0), 1.5*s, state.viewport_size)
        draw_circle_outline(rex, rey, eye_r, (0.1, 0.1, 0.1, 1.0), 1.5*s, state.viewport_size)
        
        # Pupil tracking mouse
        pupil_r = 2.8*s
        limit = eye_r - pupil_r - 0.5*s
        
        # Left pupil offset
        ldx, ldy = state.mouse_pos[0] - lex, state.mouse_pos[1] - ley
        ldist = math.hypot(ldx, ldy)
        if ldist > 0:
            lf = min(ldist * 0.03, limit)
            lex_p = lex + (ldx / ldist) * lf
            ley_p = ley + (ldy / ldist) * lf
        else:
            lex_p, ley_p = lex, ley
            
        # Right pupil offset
        rdx, rdy = state.mouse_pos[0] - rex, state.mouse_pos[1] - rey
        rdist = math.hypot(rdx, rdy)
        if rdist > 0:
            rf = min(rdist * 0.03, limit)
            rex_p = rex + (rdx / rdist) * rf
            rey_p = rey + (rdy / rdist) * rf
        else:
            rex_p, rey_p = rex, rey
            
        # Draw pupils
        draw_circle(lex_p, ley_p, pupil_r, (0.08, 0.08, 0.08, 1.0))
        draw_circle(rex_p, rey_p, pupil_r, (0.08, 0.08, 0.08, 1.0))
        
        # Reflection dot
        draw_circle(lex_p + 1.0*s, ley_p + 1.0*s, 0.8*s, (1.0, 1.0, 1.0, 1.0))
        draw_circle(rex_p + 1.0*s, rey_p + 1.0*s, 0.8*s, (1.0, 1.0, 1.0, 1.0))
        
    # 5. Eyebrows
    eb_y_l_orig = dcy + 21*s
    eb_y_r_orig = dcy + 21*s
    eb_h_l_orig = 0
    eb_h_r_orig = 0
    
    if state.expression == 'THINKING':
        eb_y_l_orig = dcy + 19*s
        eb_y_r_orig = dcy + 23*s
        eb_h_l_orig = 1.8*s
        eb_h_r_orig = -1.8*s
    elif state.is_talking:
        osc = math.sin(time.time() * 20) * 0.8 * s
        eb_y_l_orig += osc
        eb_y_r_orig += osc
        
    eb_l_pts = rotate_points([(lex_orig - 7*s, eb_y_l_orig - eb_h_l_orig), (lex_orig + 4*s, eb_y_l_orig + eb_h_l_orig)], dcx, dcy, state.rotation)
    eb_r_pts = rotate_points([(rex_orig - 4*s, eb_y_r_orig + eb_h_r_orig), (rex_orig + 7*s, eb_y_r_orig - eb_h_r_orig)], dcx, dcy, state.rotation)
    
    draw_polyline(eb_l_pts, (0.1, 0.1, 0.12, 1.0), 2.2*s, state.viewport_size)
    draw_polyline(eb_r_pts, (0.1, 0.1, 0.12, 1.0), 2.2*s, state.viewport_size)
    
    # 6. Mouth
    mx_c_orig, my_c_orig = dcx, dcy - 1.5*s
    mx_c, my_c = rotate_points([(mx_c_orig, my_c_orig)], dcx, dcy, state.rotation)[0]
    
    if state.is_talking:
        # Animating open mouth ellipse
        draw_circle(mx_c, my_c, 3.2*s, (0.1, 0.1, 0.1, 1.0))
        # Draw small tongue
        draw_circle(mx_c, my_c - 1.3*s, 1.8*s, (0.9, 0.38, 0.45, 1.0))
    elif state.expression == 'THINKING':
        m_pts = rotate_points([(mx_c_orig - 4*s, my_c_orig), (mx_c_orig, my_c_orig - 1.0*s), (mx_c_orig + 4*s, my_c_orig)], dcx, dcy, state.rotation)
        draw_polyline(m_pts, (0.1, 0.1, 0.1, 1.0), 2.0*s, state.viewport_size)
    else:
        # Happy smile curve
        m_pts = [
            (mx_c_orig - 4.5*s, my_c_orig + 1*s),
            (mx_c_orig - 2*s, my_c_orig - 2*s),
            (mx_c_orig, my_c_orig - 3.0*s),
            (mx_c_orig + 2*s, my_c_orig - 2*s),
            (mx_c_orig + 4.5*s, my_c_orig + 1*s)
        ]
        m_pts = rotate_points(m_pts, dcx, dcy, state.rotation)
        draw_polyline(m_pts, (0.1, 0.1, 0.1, 1.0), 2.2*s, state.viewport_size)

    # 7. Draw Speech Bubble
    draw_speech_bubble(dcx, dcy, s, state, context)
    
    # 8. Draw Context Menu
    draw_context_menu(state)
    
    # Force redraw on next frame if animations are active
    if (state.is_talking or 
        state.is_blinking or 
        state.nod_start_time > 0.0 or 
        state.jump_start_time > 0.0 or 
        state.is_dragging):
        context.area.tag_redraw()

# --- DRAWING BUBBLE AND MENU ---
def draw_speech_bubble(cx, cy, s, state, context):
    if not state.bubble_visible or not state.bubble_text_target:
        return
        
    font_id = 0
    font_size = int(12 * s)
    blf.size(font_id, font_size)
    
    max_w = int(185 * s)
    line_h = int(16 * s)
    padding = int(12 * s)
    
    # Calculate lines in drawing thread (safe for blf)
    current_text = state.bubble_text_target[:state.bubble_char_count]
    lines = wrap_text(current_text, max_w, font_id, font_size)
    state.bubble_lines = lines # Cache for bounds checks
    
    if not lines:
        return
        
    text_h = len(lines) * line_h
    button_area_h = int(32 * s) if state.bubble_buttons else 0
    
    bw = max_w + padding * 2
    bh = text_h + padding * 2 + button_area_h
    
    # Check if bubble is on the left
    is_left = cx > state.viewport_size[0] - 280
    
    if is_left:
        bx = cx - bw - 30*s
        by = cy + 5*s
        px, py = cx - 12*s, cy + 10*s
    else:
        bx = cx + 30*s
        by = cy + 5*s
        px, py = cx + 12*s, cy + 10*s
        
    # Bubble drop shadow
    draw_rounded_rect(bx + 2.5*s, by - 2.5*s, bw, bh, 8*s, (0.0, 0.0, 0.0, 0.14))
    
    # Bubble Background
    bg_color = (1.0, 1.0, 0.88, 1.0) # Light yellow
    draw_rounded_rect(bx, by, bw, bh, 8*s, bg_color)
    
    # Bubble Pointer
    draw_bubble_pointer(bx, by, px, py, is_left, bw, bg_color, (0.12, 0.12, 0.15, 1.0), 1.5*s, state.viewport_size)
    
    # Bubble Border
    draw_rounded_rect_outline(bx, by, bw, bh, 8*s, (0.12, 0.12, 0.15, 1.0), 1.5*s, state.viewport_size)
    
    # Draw text lines
    blf.color(font_id, 0.08, 0.08, 0.1, 1.0)
    for i, line in enumerate(lines):
        lx = bx + padding
        ly = by + bh - padding - (i + 1) * line_h + int(1.5 * s)
        blf.position(font_id, lx, ly, 0)
        blf.draw(font_id, line)
        
    # Draw buttons
    if state.bubble_buttons:
        btn_count = len(state.bubble_buttons)
        btn_w = int((bw - padding * 2 - (btn_count - 1) * 8 * s) / btn_count)
        btn_h = int(22 * s)
        btn_y = by + padding
        
        for idx, btn in enumerate(state.bubble_buttons):
            btn_x = bx + padding + idx * (btn_w + int(8 * s))
            btn['rect'] = (btn_x, btn_y, btn_w, btn_h)
            
            mx, my = state.mouse_pos
            is_hover = (btn_x <= mx <= btn_x + btn_w) and (btn_y <= my <= btn_y + btn_h)
            
            if btn.get('type') == 'next':
                bg = (0.2, 0.52, 0.33, 1.0) if not is_hover else (0.24, 0.62, 0.4, 1.0)
                tc = (1.0, 1.0, 1.0, 1.0)
            elif btn.get('type') == 'exit':
                bg = (0.7, 0.22, 0.22, 1.0) if not is_hover else (0.8, 0.28, 0.28, 1.0)
                tc = (1.0, 1.0, 1.0, 1.0)
            else:
                bg = (0.83, 0.83, 0.85, 1.0) if not is_hover else (0.88, 0.88, 0.9, 1.0)
                tc = (0.1, 0.1, 0.12, 1.0)
                
            draw_rounded_rect(btn_x, btn_y, btn_w, btn_h, 4*s, bg)
            draw_rounded_rect_outline(btn_x, btn_y, btn_w, btn_h, 4*s, (0.12, 0.12, 0.15, 1.0), 1.0*s, state.viewport_size)
            
            blf.size(font_id, int(11 * s))
            tw, th = blf.dimensions(font_id, btn['text'])
            tx = btn_x + (btn_w - tw) / 2
            ty = btn_y + (btn_h - th) / 2 + int(1 * s)
            blf.color(font_id, *tc)
            blf.position(font_id, tx, ty, 0)
            blf.draw(font_id, btn['text'])

def get_context_menu_bounds(state):
    s = 1.5
    font_id = 0
    font_size = int(11 * s)
    blf.size(font_id, font_size)
    
    # Calculate maximum text width across all items dynamically
    max_tw = int(150 * s)
    for item in state.menu_items:
        tw, th = blf.dimensions(font_id, item['text'])
        if tw > max_tw:
            max_tw = tw
            
    padding = int(5 * s)
    menu_w = int(max_tw + 34 * s) # Room for text, icon padding, and scrollbar
    
    item_h = int(24 * s)
    max_visible = 10
    num_visible = min(len(state.menu_items), max_visible)
    menu_h = num_visible * item_h + padding * 2
    
    vw, vh = state.viewport_size
    mx, my = state.menu_x, state.menu_y
    
    # Horizontal positioning: fit inside viewport
    if mx + menu_w > vw - 10:
        x = max(10, mx - menu_w)
    else:
        x = max(10, mx)
    x = min(vw - menu_w - 10, max(10, x))
        
    # Vertical positioning: fit inside viewport
    if my - menu_h < 10:
        y = min(vh - 10, my + menu_h)
    else:
        y = min(vh - 10, my)
    y = min(vh - 10, max(menu_h + 10, y))
        
    return x, y, menu_w, menu_h, item_h, padding, max_visible, num_visible

def draw_context_menu(state):
    if not state.menu_visible or not state.menu_items:
        return
        
    s = 1.5
    font_id = 0
    font_size = int(11 * s)
    blf.size(font_id, font_size)
    
    x, y, menu_w, menu_h, item_h, padding, max_visible, num_visible = get_context_menu_bounds(state)
    items = state.menu_items
    total_items = len(items)
    
    # Clamp scroll offset
    max_scroll = max(0, total_items - max_visible)
    state.menu_scroll_offset = max(0, min(state.menu_scroll_offset, max_scroll))
    scroll = state.menu_scroll_offset
    
    # Drop shadow
    draw_rounded_rect(x + 2.5*s, y - menu_h - 2.5*s, menu_w, menu_h, 6*s, (0.0, 0.0, 0.0, 0.22))
    # Background
    bg_color = (0.11, 0.12, 0.14, 0.96)
    draw_rounded_rect(x, y - menu_h, menu_w, menu_h, 6*s, bg_color)
    draw_rounded_rect_outline(x, y - menu_h, menu_w, menu_h, 6*s, (0.28, 0.28, 0.32, 1.0), 1.0*s, state.viewport_size)
    
    # Visible items slice
    visible_items = items[scroll : scroll + num_visible]
    
    # Hover highlight
    if state.menu_hover_idx != -1:
        rel_idx = state.menu_hover_idx - scroll
        if 0 <= rel_idx < num_visible:
            hy = y - padding - (rel_idx + 1) * item_h
            draw_rounded_rect(x + int(2*s), hy + int(0.5*s), menu_w - int(10*s), item_h - int(1*s), 4*s, (0.18, 0.44, 0.75, 0.85))
            
    # Items text rendering
    for rel_idx, item in enumerate(visible_items):
        abs_idx = scroll + rel_idx
        tx = x + int(10 * s)
        ty = y - padding - (rel_idx + 1) * item_h + int(5 * s)
        if abs_idx == state.menu_hover_idx:
            blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
        else:
            blf.color(font_id, 0.84, 0.84, 0.87, 1.0)
        blf.position(font_id, tx, ty, 0)
        blf.draw(font_id, item['text'])
        
    # Scrollbar indicator
    if total_items > max_visible:
        bar_w = int(4 * s)
        bar_x = x + menu_w - bar_w - int(3 * s)
        track_h = menu_h - padding * 2
        thumb_h = max(int(16 * s), int(track_h * (max_visible / total_items)))
        thumb_y = y - padding - thumb_h - int((track_h - thumb_h) * (scroll / max_scroll))
        draw_rounded_rect(bar_x, thumb_y, bar_w, thumb_h, 2*s, (0.45, 0.48, 0.55, 0.8))

# --- ACTIVE OPERATOR REFERENCE ---
_active_clippy_operator = None

# --- MODAL OPERATOR CLASS ---
class CLIPPY_OT_companion(bpy.types.Operator):
    bl_idname = "view3d.clippy_companion"
    bl_label = "Clippy Companion"
    
    should_exit = False
    
    def cancel_modal(self):
        self.should_exit = True

    def is_mouse_over_clippy(self, mx, my):
        dist = math.hypot(mx - self.state.x, my - self.state.y)
        return dist < (35.0 * 1.5)
        
    def is_mouse_over_bubble(self, mx, my):
        if not self.state.bubble_visible or not self.state.bubble_lines:
            return False
        cx = self.state.x
        cy = self.state.y
        s = 1.5
        max_w = int(185 * s)
        line_h = int(16 * s)
        padding = int(12 * s)
        text_h = len(self.state.bubble_lines) * line_h
        button_area_h = int(32 * s) if self.state.bubble_buttons else 0
        bw = max_w + padding * 2
        bh = text_h + padding * 2 + button_area_h
        
        is_left = cx > self.state.viewport_size[0] - 280
        if is_left:
            bx = cx - bw - 30*s
        else:
            bx = cx + 30*s
        by = cy + 5*s
        return (bx <= mx <= bx + bw) and (by <= my <= by + bh)

    def set_bubble_text(self, text):
        self.state.bubble_text_target = text
        self.state.bubble_char_count = 0
        self.state.bubble_lines = []
        self.state.last_char_time = time.time()
        self.state.is_talking = True

    def close_bubble(self):
        self.state.bubble_visible = False
        self.state.bubble_text_target = ""
        self.state.bubble_lines = []
        self.state.bubble_buttons = []
        self.state.is_talking = False

    def toggle_language(self):
        if self.state.language == 'EN':
            self.state.language = 'PL'
            msg = "Język został zmieniony na Polski! 🇵🇱 Wybierz samouczek z menu."
        else:
            self.state.language = 'EN'
            msg = "Language changed to English! 🇬🇧 Pick a tutorial from the menu."
        self.setup_context_menu()
        self.set_bubble_text(msg)
        self.state.expression = 'HAPPY'
        self.state.bubble_buttons = [
            {
                'text': 'Zamknij' if self.state.language == 'PL' else 'Close',
                'type': 'close',
                'action': lambda ctx: self.close_bubble()
            }
        ]
        self.state.bubble_visible = True
        self.trigger_nod()

    def show_random_tip(self):
        lang = self.state.language
        tips_list = TIPS.get(lang, TIPS['EN'])
        tip = random.choice(tips_list)
        self.state.expression = 'HAPPY'
        self.set_bubble_text(tip)
        self.state.bubble_buttons = [
            {
                'text': 'Zamknij' if lang == 'PL' else 'Close',
                'type': 'close',
                'action': lambda ctx: self.close_bubble()
            }
        ]
        self.state.bubble_visible = True

    def trigger_nod(self):
        self.state.nod_start_time = time.time()

    def trigger_celebrate(self):
        self.state.jump_start_time = time.time()

    def start_tutorial(self, tut_id):
        if tut_id in TUTORIALS:
            self.state.active_tutorial = TUTORIALS[tut_id]
            self.state.tutorial_step_idx = 0
            self.show_tutorial_step()
            self.trigger_nod()
            
    def show_tutorial_step(self):
        tut = self.state.active_tutorial
        lang = self.state.language
        step = tut['steps'][self.state.tutorial_step_idx]
        text_dict = step['text']
        text = text_dict.get(lang, text_dict.get('EN', ''))
        
        self.state.expression = 'THINKING' if step.get('check') else 'HAPPY'
        self.set_bubble_text(text)
        
        exit_lbl = "Wyjdź" if lang == 'PL' else "Exit"
        back_lbl = "Wstecz" if lang == 'PL' else "Back"
        is_last = self.state.tutorial_step_idx == len(tut['steps']) - 1
        next_lbl = ("Gotowe" if is_last else "Dalej") if lang == 'PL' else ("Done" if is_last else "Next")
        
        buttons = [
            {
                'text': exit_lbl,
                'type': 'exit',
                'action': lambda ctx: self.exit_tutorial()
            }
        ]
        if self.state.tutorial_step_idx > 0:
            buttons.append({
                'text': back_lbl,
                'type': 'back',
                'action': lambda ctx: self.prev_tutorial_step()
            })
            
        buttons.append({
            'text': next_lbl,
            'type': 'next',
            'action': lambda ctx: self.next_tutorial_step()
        })
        self.state.bubble_buttons = buttons
        self.state.bubble_visible = True

    def prev_tutorial_step(self):
        if self.state.tutorial_step_idx > 0:
            self.state.tutorial_step_idx -= 1
            self.show_tutorial_step()
            self.trigger_nod()
            
    def next_tutorial_step(self):
        tut = self.state.active_tutorial
        if self.state.tutorial_step_idx < len(tut['steps']) - 1:
            self.state.tutorial_step_idx += 1
            self.show_tutorial_step()
            self.trigger_nod()
        else:
            self.exit_tutorial()
            self.trigger_celebrate()
            
    def exit_tutorial(self):
        self.state.active_tutorial = None
        self.state.tutorial_step_idx = 0
        self.close_bubble()

    def setup_context_menu(self):
        lang = self.state.language
        if lang == 'PL':
            self.state.menu_items = [
                {'text': "🎓 Samouczek: Wprowadzenie", 'action': lambda ctx: self.start_tutorial("intro")},
                {'text': "🛋️ Samouczek: Poduszka", 'action': lambda ctx: self.start_tutorial("cushion")},
                {'text': "💡 Samouczek: Światło i Kamera", 'action': lambda ctx: self.start_tutorial("lighting")},
                {'text': "🎨 Samouczek: Materiały", 'action': lambda ctx: self.start_tutorial("materials")},
                {'text': "✂️ Samouczek: Inset & Extrude", 'action': lambda ctx: self.start_tutorial("extrude")},
                {'text': "🗿 Samouczek: Rzeźbienie", 'action': lambda ctx: self.start_tutorial("sculpting")},
                {'text': "🔧 Samouczek: Subdivision", 'action': lambda ctx: self.start_tutorial("modifiers")},
                {'text': "🎬 Samouczek: Animacja", 'action': lambda ctx: self.start_tutorial("animation")},
                {'text': "🗺️ Samouczek: Rozwijanie UV", 'action': lambda ctx: self.start_tutorial("uv_unwrap")},
                {'text': "🌐 Samouczek: Węzły Shadera", 'action': lambda ctx: self.start_tutorial("nodes")},
                {'text': "👗 Samouczek: Symulacja Tkaniny", 'action': lambda ctx: self.start_tutorial("cloth")},
                {'text': "✨ Samouczek: Cząsteczki", 'action': lambda ctx: self.start_tutorial("particles")},
                {'text': "✏️ Samouczek: 2D Grease Pencil", 'action': lambda ctx: self.start_tutorial("grease_pencil")},
                {'text': "🎲 Samouczek: Ciała Sztywne", 'action': lambda ctx: self.start_tutorial("rigid_body")},
                {'text': "📐 Samouczek: Modyfikator Bevel", 'action': lambda ctx: self.start_tutorial("bevel_modifier")},
                {'text': "💡 Zapytaj o Wskazówkę", 'action': lambda ctx: self.show_random_tip()},
                {'text': "🇵🇱 Język: Polski (Zmień na 🇬🇧)", 'action': lambda ctx: self.toggle_language()},
                {'text': "📍 Zresetuj Pozycję", 'action': lambda ctx: self.reset_position()},
                {'text': "❌ Ukryj Clippy'ego", 'action': lambda ctx: self.cancel_modal()}
            ]
        else:
            self.state.menu_items = [
                {'text': "🎓 Tutorial: Intro to Blender", 'action': lambda ctx: self.start_tutorial("intro")},
                {'text': "🛋️ Tutorial: Cushion Model", 'action': lambda ctx: self.start_tutorial("cushion")},
                {'text': "💡 Tutorial: Lighting & Camera", 'action': lambda ctx: self.start_tutorial("lighting")},
                {'text': "🎨 Tutorial: Materials & Shading", 'action': lambda ctx: self.start_tutorial("materials")},
                {'text': "✂️ Tutorial: Inset & Extrude", 'action': lambda ctx: self.start_tutorial("extrude")},
                {'text': "🗿 Tutorial: Sculpting Basics", 'action': lambda ctx: self.start_tutorial("sculpting")},
                {'text': "🔧 Tutorial: Subdivision Surface", 'action': lambda ctx: self.start_tutorial("modifiers")},
                {'text': "🎬 Tutorial: Keyframe Animation", 'action': lambda ctx: self.start_tutorial("animation")},
                {'text': "🗺️ Tutorial: UV Unwrapping", 'action': lambda ctx: self.start_tutorial("uv_unwrap")},
                {'text': "🌐 Tutorial: Shader Nodes", 'action': lambda ctx: self.start_tutorial("nodes")},
                {'text': "👗 Tutorial: Cloth Simulation", 'action': lambda ctx: self.start_tutorial("cloth")},
                {'text': "✨ Tutorial: Particle System", 'action': lambda ctx: self.start_tutorial("particles")},
                {'text': "✏️ Tutorial: 2D Grease Pencil", 'action': lambda ctx: self.start_tutorial("grease_pencil")},
                {'text': "🎲 Tutorial: Rigid Body Physics", 'action': lambda ctx: self.start_tutorial("rigid_body")},
                {'text': "📐 Tutorial: Bevel Modifier", 'action': lambda ctx: self.start_tutorial("bevel_modifier")},
                {'text': "💡 Ask for a Tip", 'action': lambda ctx: self.show_random_tip()},
                {'text': "🇬🇧 Language: English (Switch to 🇵🇱)", 'action': lambda ctx: self.toggle_language()},
                {'text': "📍 Reset Position", 'action': lambda ctx: self.reset_position()},
                {'text': "❌ Hide Clippy", 'action': lambda ctx: self.cancel_modal()}
            ]

    def reset_position(self):
        self.state.x = self.state.viewport_size[0] - 120
        self.state.y = 110
        self.trigger_nod()

    def update_animations(self, context):
        state = self.state
        now = time.time()
        
        # Typing bubble effect
        if state.bubble_visible and state.bubble_text_target:
            if state.bubble_char_count < len(state.bubble_text_target):
                if now - state.last_char_time > 0.018:
                    state.bubble_char_count += 1
                    state.last_char_time = now
                    state.is_talking = True
            else:
                if state.is_talking:
                    state.is_talking = False
                    
        # Blinking eye effect
        if now > state.next_blink_time:
            state.is_blinking = True
            state.next_blink_time = now + random.uniform(3.5, 6.5)
            state.blink_end_time = now + state.blink_duration
        if state.is_blinking and now > state.blink_end_time:
            state.is_blinking = False
            
        # Real-time state check for tutorials
        if state.active_tutorial and not state.is_talking:
            step = state.active_tutorial['steps'][state.tutorial_step_idx]
            check_func = step.get('check')
            if check_func:
                try:
                    if check_func(context):
                        self.next_tutorial_step()
                except Exception:
                    pass

    # --- MODAL SYSTEM ENGINES ---
    def invoke(self, context, event):
        global _active_clippy_operator
        
        # If already running, toggle off by cancelling
        if _active_clippy_operator is not None:
            _active_clippy_operator.cancel_modal()
            _active_clippy_operator = None
            context.window_manager.clippy_running = False
            context.area.tag_redraw()
            return {'CANCELLED'}
            
        # Initialize state
        self.state = ClippyState()
        
        # Find the window region of the 3D viewport
        window_width = context.area.width
        window_height = context.area.height
        for r in context.area.regions:
            if r.type == 'WINDOW':
                window_width = r.width
                window_height = r.height
                break
                
        self.state.x = window_width - 120
        self.state.y = 110
        self.state.viewport_size = (window_width, window_height)
        self.setup_context_menu()
        
        # Add drawing handler
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback, (self, context), 'WINDOW', 'POST_PIXEL'
        )
        
        # Add background animation timer
        self._timer = context.window_manager.event_timer_add(0.016, window=context.window)
        
        context.window_manager.modal_handler_add(self)
        context.window_manager.clippy_running = True
        _active_clippy_operator = self
        
        print(f"[Clippy] Operator Summoned! Region size: {window_width}x{window_height}, Clippy at ({self.state.x}, {self.state.y})")
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        global _active_clippy_operator
        
        # Force check for programmatic termination
        if self.should_exit:
            # Cleanup
            context.window_manager.event_timer_remove(self._timer)
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            context.window_manager.clippy_running = False
            if _active_clippy_operator == self:
                _active_clippy_operator = None
            context.area.tag_redraw()
            return {'FINISHED'}
            
        # Update mouse coordinates
        if event.type == 'MOUSEMOVE':
            self.state.mouse_pos = (event.mouse_region_x, event.mouse_region_y)
            
        # Animation updates via Timer (draw thread updates states, timer drives breathing redraw)
        if event.type == 'TIMER':
            context.area.tag_redraw()
            return {'RUNNING_MODAL'}
            
        # Mouse interactions
        mx, my = event.mouse_region_x, event.mouse_region_y
        
        # 1. Hover & Scroll updates for context menu
        if self.state.menu_visible:
            x, y, menu_w, menu_h, item_h, padding, max_visible, num_visible = get_context_menu_bounds(self.state)
            
            within_menu_x = x <= mx <= x + menu_w
            within_menu_y = y - menu_h <= my <= y
            
            if within_menu_x and within_menu_y:
                max_scroll = max(0, len(self.state.menu_items) - max_visible)
                if event.type == 'WHEELUPMOUSE':
                    self.state.menu_scroll_offset = max(0, self.state.menu_scroll_offset - 1)
                    context.area.tag_redraw()
                    return {'RUNNING_MODAL'}
                elif event.type == 'WHEELDOWNMOUSE':
                    self.state.menu_scroll_offset = min(max_scroll, self.state.menu_scroll_offset + 1)
                    context.area.tag_redraw()
                    return {'RUNNING_MODAL'}
                    
                rel_idx = int((y - padding - my) / item_h)
                if 0 <= rel_idx < num_visible:
                    self.state.menu_hover_idx = self.state.menu_scroll_offset + rel_idx
                else:
                    self.state.menu_hover_idx = -1
            else:
                self.state.menu_hover_idx = -1
                
        # 2. Clicks on Context Menu
        if self.state.menu_visible:
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if self.state.menu_hover_idx != -1:
                    # Execute selected menu action
                    self.state.menu_items[self.state.menu_hover_idx]['action'](context)
                self.state.menu_visible = False
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
            elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
                # Dismiss menu on click outside or escape
                self.state.menu_visible = False
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
                
        # 3. Clicks on Speech Bubble Buttons
        if self.state.bubble_visible and self.state.bubble_buttons:
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                for btn in self.state.bubble_buttons:
                    if 'rect' in btn:
                        bx, by, bw, bh = btn['rect']
                        if bx <= mx <= bx + bw and by <= my <= by + bh:
                            btn['action'](context)
                            context.area.tag_redraw()
                            return {'RUNNING_MODAL'}
                            
        # 4. Drag & Drop or Click (Tip) on Clippy himself
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                over = self.is_mouse_over_clippy(mx, my)
                dist = math.hypot(mx - self.state.x, my - self.state.y)
                print(f"[Clippy] Left-click PRESS at ({mx}, {my}). Clippy position: ({self.state.x}, {self.state.y}), dist={dist:.1f}, Over={over}")
                
                # Close context menu if clicked outside it
                self.state.menu_visible = False
                
                # Check click on Clippy
                if over:
                    self.state.is_dragging = True
                    self.state.drag_offset_x = self.state.x - mx
                    self.state.drag_offset_y = self.state.y - my
                    self.state.click_start_time = time.time()
                    self.state.click_start_pos = (mx, my)
                    context.area.tag_redraw()
                    return {'RUNNING_MODAL'}
                    
            elif event.value == 'RELEASE':
                if self.state.is_dragging:
                    self.state.is_dragging = False
                    
                    dx = mx - self.state.click_start_pos[0]
                    dy = my - self.state.click_start_pos[1]
                    drag_dist = math.hypot(dx, dy)
                    duration = time.time() - self.state.click_start_time
                    print(f"[Clippy] Left-click RELEASE at ({mx}, {my}). drag_dist={drag_dist:.1f}, duration={duration:.3f}")
                    
                    # Quick tap without drag -> trigger tip!
                    if drag_dist < 12.0 and duration < 0.45:
                        print("[Clippy] Left-click tap detected! Showing random tip...")
                        self.show_random_tip()
                    context.area.tag_redraw()
                    return {'RUNNING_MODAL'}
                    
        elif event.type == 'MOUSEMOVE' and self.state.is_dragging:
            # Update Clippy coordinates
            self.state.x = mx + self.state.drag_offset_x
            self.state.y = my + self.state.drag_offset_y
            
            # Find window region size
            window_width = context.area.width
            window_height = context.area.height
            for r in context.area.regions:
                if r.type == 'WINDOW':
                    window_width = r.width
                    window_height = r.height
                    break
            
            # Constrain to viewport region bounds
            self.state.x = max(30, min(self.state.x, window_width - 30))
            self.state.y = max(40, min(self.state.y, window_height - 40))
            context.area.tag_redraw()
            return {'RUNNING_MODAL'}
            
        # 5. Right Click on Clippy (opens context menu)
        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            over = self.is_mouse_over_clippy(mx, my)
            dist = math.hypot(mx - self.state.x, my - self.state.y)
            print(f"[Clippy] Right-click PRESS at ({mx}, {my}). Clippy position: ({self.state.x}, {self.state.y}), dist={dist:.1f}, Over={over}")
            if over:
                print("[Clippy] Right-click detected! Opening context menu.")
                self.state.menu_x = mx
                self.state.menu_y = my
                self.state.menu_visible = True
                self.state.menu_scroll_offset = 0 # Reset scroll on open
                self.state.bubble_visible = False # Dismiss bubble
                self.state.menu_hover_idx = -1
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
                
        # 6. Esc key cancels operator
        if event.type == 'ESC' and event.value == 'PRESS':
            self.cancel_modal()
            return {'RUNNING_MODAL'}
            
        # Check mouse over Clippy UI structures to set grabbing cursor
        if self.is_mouse_over_clippy(mx, my):
            # Change cursor to hand grab icon
            context.window.cursor_modal_set('HAND')
        else:
            context.window.cursor_modal_restore()
            
        # Consume any clicks inside the speech bubble to avoid clicking viewport objects
        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'} and self.is_mouse_over_bubble(mx, my):
            return {'RUNNING_MODAL'}
            
        # Pass through all other events to let Blender be fully functional!
        return {'PASS_THROUGH'}

# --- SIDEBAR PANEL CLASS ---
class CLIPPY_PT_panel(bpy.types.Panel):
    bl_label = "Clippy Companion"
    bl_idname = "CLIPPY_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Clippy'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        is_running = getattr(wm, "clippy_running", False)
        
        col = layout.column(align=True)
        col.scale_y = 1.3
        
        if not is_running:
            col.operator("view3d.clippy_companion", text="Summon Clippy", icon='USER')
        else:
            col.operator("view3d.clippy_companion", text="Dismiss Clippy", icon='PANEL_CLOSE')

# --- ADDON REGISTRATION ---
def register():
    bpy.utils.register_class(CLIPPY_OT_companion)
    bpy.utils.register_class(CLIPPY_PT_panel)
    bpy.types.WindowManager.clippy_running = bpy.props.BoolProperty(default=False)

def unregister():
    global _active_clippy_operator
    if _active_clippy_operator is not None:
        try:
            _active_clippy_operator.cancel_modal()
        except Exception:
            pass
        _active_clippy_operator = None
        
    bpy.utils.unregister_class(CLIPPY_PT_panel)
    bpy.utils.unregister_class(CLIPPY_OT_companion)
    try:
        del bpy.types.WindowManager.clippy_running
    except Exception:
        pass

if __name__ == "__main__":
    register()
