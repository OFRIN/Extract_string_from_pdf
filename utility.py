
import queue

#######################################################
# for PPTX
#######################################################
def get_size(shape):
    return shape.width * shape.height

def get_max_shape(shapes):
    max_size = -1
    max_shape = None
    
    for shape in shapes:
        if not shape.has_text_frame:
            continue
        
        size = get_size(shape)
        if max_shape is None or size > max_size:
            max_size = get_size(shape)
            max_shape = shape
    
    return max_shape

def check_slide(slide, feature):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        
        for data in simple_parsing(shape.text):
            if feature in data:
                return True

    return False

#######################################################
# for PDF
#######################################################
def check_page(page, feature):
    text = page.extract_text()
    if text is None:
        return None
        
    return feature in page.extract_text()

#######################################################
# for text processing
#######################################################
def remove_frontal_space(text):
    for i in range(len(text)):
        if ord(text[i]) != 32:
            return text[i:]

def simple_parsing(text):
    return [data for data in text.split('\n') if data != '']

def script_parsing(text):
    parsed_dataset = []
    for data in text.split('\n'):
        if data == '':
            continue
        
        if ':' in data:
            parsed_dataset.append(data)
        else:
            if '#' in data:
                continue
            
            data = remove_frontal_space(data)
            if data is None:
                continue
            
            last_char = parsed_dataset[-1][-1]

            if last_char == ' ':
                parsed_dataset[-1] += data
            else:
                parsed_dataset[-1] += ' ' + data

    return parsed_dataset

def pattern_parsing_using_indices(text, selected_indices=None):
    pattern_dataset = []
    dataset = [remove_frontal_space(data) for data in text.split('\n')[3:] if data != '' and len(data) > 1]

    if len(selected_indices) == 0:
        for index, data in enumerate(dataset):
            if '_' in data:
                selected_indices.append(index)
            else:
                pattern_dataset.append(data)

        if len(pattern_dataset) % 2 == 1:
            pattern_dataset = pattern_dataset[1:]
            
        return pattern_dataset
    
    else:
        return [dataset[index] for index in selected_indices]
