from flask import Flask, jsonify, request

app = Flask(__name__) # __name__ tells Flask where to find the app
 
# Our 'fake database' — a plain Python list
students = [
 {"id": 1, "name": "Ali", "grade": "A"},
 {"id": 2, "name": "Sara", "grade": "B"},
 ]

@app.route('/students', methods=['GET'])
def get_all_students():
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_one_student(student_id):
    for student in students:
        if student['id'] == student_id:
           return jsonify(student)
    # Nothing found — return 404
    return jsonify({'error': 'Student not found'}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json() # read the JSON body the caller sent
 
    if not data or 'name' not in data:
       return jsonify({'error': 'name is required'}), 400
 
    new_student = {
        'id': len(students) + 1, # simple auto-increment
        'name': data['name'],
        'grade': data.get('grade', 'N/A') # optional field
    }
    students.append(new_student)
    return jsonify(new_student), 201 # 201 = Created

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    for student in students:
        if student['id'] == student_id:
            student['name'] = data.get('name', student['name'])
            student['grade'] = data.get('grade', student['grade'])
            return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    for i, student in enumerate(students):
        if student['id'] == student_id:
            del students[i]
            return jsonify({'message': 'Student deleted'})
    return jsonify({'error': 'Student not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)