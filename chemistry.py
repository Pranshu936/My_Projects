import cv2
import mediapipe as mp
import time

elements_first = ["O", "Se", "Ca", "He", "S", "N", "Mg", "C", "Cl"]
elements_second = ["H", "Na", "Bi"]
compounds = {
    ("H", "O"): "H2O",
    ("Na", "Cl"): "NaCl",
    ("Mg", "O"): "MgO",
    ("C", "O"): "CO2",
    ("H", "Cl"): "HCl",
    ("Ca", "O"): "CaO",
    ("Na", "O"): "Na2O",
    ("S", "O"): "SO2",
    ("N", "O"): "NO2",
}
descriptions = {
    "H2O": """Water (H2O) is a vital compound, crucial for all forms of life on Earth. It serves as a universal solvent and is central to biochemical reactions and temperature regulation in organisms.""",
    "NaCl": """Sodium chloride (NaCl), commonly known as table salt, is essential for human health. It regulates fluid balance, nerve function, and is widely used in food, de-icing, and various industrial processes.""",
    "MgO": """Magnesium oxide (MgO) is a white, crystalline powder widely used in medicine as an antacid and laxative. Industrially, it is valued for its high melting point and used in refractory materials and fertilizers.""",
    "CO2": """Carbon dioxide (CO2) is a colorless, odorless gas and a key component of Earth's carbon cycle. It is essential for photosynthesis in plants and is a significant greenhouse gas contributing to global warming.""",
    "HCl": """Hydrochloric acid (HCl) is a strong, corrosive acid used in various industries, including cleaning, pickling metals, and producing fertilizers and dyes. In the body, it aids digestion in the stomach.""",
    "CaO": """Calcium oxide (CaO), also known as quicklime, is a white, caustic substance used in cement, soil stabilization, and water treatment. It reacts exothermically with water to produce calcium hydroxide.""",
    "Na2O": """Sodium oxide (Na2O) is a solid compound used primarily in glass and ceramic manufacturing, where it helps to lower melting points and improve chemical stability.""",
    "SO2": """Sulfur dioxide (SO₂) is a pungent gas commonly produced by volcanic activity and industrial processes. It is used to produce sulfuric acid and as a preservative in foods and wines.""",
    "NO2": """Nitrogen dioxide (NO2) is a reddish-brown gas with a sharp odor, produced by combustion processes. It is a significant air pollutant and contributes to smog and acid rain formation."""
}



mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

selected_element1 = None
selected_element2 = None
result = None
description = ""


dwell_time = 0.5  
frame_count_threshold = 5  
frame_counter = 0  
hover_start_time = None  

def is_within_box(x, y, box_x, box_y, box_width, box_height):
    return box_x <= x <= box_x + box_width and box_y <= y <= box_y + box_height

def get_selected_element(x, y):

    for i, element in enumerate(elements_first):
        box_x = i * 120 + 50
        box_y = 10
        if is_within_box(x, y, box_x, box_y, 100, 80):
            return element

    for i, element in enumerate(elements_second):
        box_x = 50
        box_y = i * 100 + 150
        if is_within_box(x, y, box_x, box_y, 100, 80):
            return element
    return None

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    for i, element in enumerate(elements_first):
        x_pos = i * 120 + 50
        y_pos = 10
        cv2.rectangle(img, (x_pos, y_pos), (x_pos + 100, y_pos + 80), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, element, (x_pos + 20, y_pos + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    for i, element in enumerate(elements_second):
        x_pos = 50
        y_pos = i * 100 + 150
        cv2.rectangle(img, (x_pos, y_pos), (x_pos + 100, y_pos + 80), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, element, (x_pos + 20, y_pos + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.rectangle(img, (200, 100), (1220, 200), (0, 255, 0), 2)
    if selected_element1:
        cv2.putText(img, f"{selected_element1} + ", (220, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    if selected_element2:
        cv2.putText(img, selected_element2, (390, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    if result:
        cv2.putText(img, f" = {result}", (470, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    if description:
        y_offset = 230
        for i, line in enumerate(description.splitlines()):
            cv2.putText(img, line, (220, y_offset + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            h, w, _ = img.shape
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            tip_x, tip_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            cv2.circle(img, (tip_x, tip_y), 10, (255, 0, 0), cv2.FILLED)

            selected_element = get_selected_element(tip_x, tip_y)
            if selected_element:
                if hover_start_time is None:
                    hover_start_time = time.time()
                    frame_counter = 1
                else:
                    frame_counter += 1
                    elapsed_time = time.time() - hover_start_time

                    if frame_counter >= frame_count_threshold and elapsed_time >= dwell_time:
                        if not selected_element1:
                            selected_element1 = selected_element
                        elif not selected_element2:
                            selected_element2 = selected_element
                            result = compounds.get((selected_element1, selected_element2), "No Match")
                            description = descriptions.get(result, "No information available for this compound.")
                        hover_start_time = None  
            else:
                hover_start_time = None
                frame_counter = 0

    cv2.putText(img, "Press 'C' to clear", (200, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        selected_element1, selected_element2 = None, None
        result, description = None, ""

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (1000, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
