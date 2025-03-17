"""Script cleans the Json file of Webscrapped courses"""

import json


def observe_courses(courses: list[dict]) -> dict:
    """
        Method returns all duplicate courses
    """
    faulty_courses = []
    memo = {}

    for course in courses:
        if course['title'] in memo:
            memo[course['title']].append(course)
        else:
            memo[course['title']] = [course]
            if course.get('url', None) is None:
                faulty_courses.append(course)
    duplicate_courses = {k:v for k,v in memo.items() if len(v) > 1}
    return duplicate_courses, faulty_courses


if __name__ == "__main__":
    with open('database_config/default_courses_collection.json',
                encoding="UTF-8") as file_data:
        courses_data = json.load(file_data)
    if courses_data is not None:
        duplicate_courses, faulty_courses = observe_courses(courses_data)
        print("Faulty Courses: ")
        print(json.dumps(faulty_courses, indent=2))
        print("Duplicate Courses: ")
        print(json.dumps(duplicate_courses, indent=2))
        print("Total courses that are faulty courses: ", len(faulty_courses))
        print("Total courses that are duplicate courses: ", len(duplicate_courses))
