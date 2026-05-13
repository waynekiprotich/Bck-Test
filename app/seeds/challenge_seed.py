from datetime import date, timedelta
from app.extensions import db
from app.models.challenge import Challenge, TestCase, WeeklyChallenge


def seed_challenges():
    challenges_data = [
        {
            "title": "Two Sum",
            "slug": "two-sum",
            "description": (
                "Given an array of integers `nums` and an integer `target`, "
                "return the indices of the two numbers that add up to `target`.\n\n"
                "Input: nums = [2, 7, 11, 15], target = 9\n"
                "Output: [0, 1]"
            ),
            "difficulty": "Easy",
            "points_reward": 50,
            "is_practice": True,
            "starter_code_python": (
                "def two_sum(nums, target):\n"
                "    # Your code here\n"
                "    pass\n\n"
                "# Read input\n"
                "line = input().split()\n"
                "nums = list(map(int, line[:-1]))\n"
                "target = int(line[-1])\n"
                "print(two_sum(nums, target))"
            ),
            "starter_code_javascript": (
                "function twoSum(nums, target) {\n"
                "    // Your code here\n"
                "}\n\n"
                "const lines = require('fs').readFileSync('/dev/stdin','utf8').trim().split(' ');\n"
                "const target = parseInt(lines.pop());\n"
                "const nums = lines.map(Number);\n"
                "console.log(JSON.stringify(twoSum(nums, target)));"
            ),
            "test_cases": [
                {"input_data": "2 7 11 15 9", "expected_output": "[0, 1]", "is_hidden": False},
                {"input_data": "3 2 4 6",     "expected_output": "[1, 2]", "is_hidden": False},
                {"input_data": "3 3 6",        "expected_output": "[0, 1]", "is_hidden": True},
            ],
        },
        {
            "title": "Valid Parentheses",
            "slug": "valid-parentheses",
            "description": (
                "Given a string containing only '(', ')', '{', '}', '[', ']', "
                "determine if the input string is valid.\n\n"
                "A string is valid if:\n"
                "- Open brackets must be closed by the same type of brackets.\n"
                "- Open brackets must be closed in the correct order.\n\n"
                "Input: s = '()[]{}'\nOutput: true"
            ),
            "difficulty": "Easy",
            "points_reward": 50,
            "is_practice": True,
            "starter_code_python": (
                "def is_valid(s):\n"
                "    # Your code here\n"
                "    pass\n\n"
                "s = input()\n"
                "print(str(is_valid(s)).lower())"
            ),
            "starter_code_javascript": (
                "function isValid(s) {\n"
                "    // Your code here\n"
                "}\n\n"
                "const s = require('fs').readFileSync('/dev/stdin','utf8').trim();\n"
                "console.log(isValid(s));"
            ),
            "test_cases": [
                {"input_data": "()",     "expected_output": "true",  "is_hidden": False},
                {"input_data": "()[]{}","expected_output": "true",  "is_hidden": False},
                {"input_data": "(]",    "expected_output": "false", "is_hidden": False},
                {"input_data": "([)]",  "expected_output": "false", "is_hidden": True},
                {"input_data": "{[]}",  "expected_output": "true",  "is_hidden": True},
            ],
        },
        {
            "title": "Reverse a String",
            "slug": "reverse-string",
            "description": (
                "Write a function that reverses a string.\n\n"
                "Input: 'hello'\nOutput: 'olleh'"
            ),
            "difficulty": "Easy",
            "points_reward": 50,
            "is_practice": True,
            "starter_code_python": (
                "def reverse_string(s):\n"
                "    # Your code here\n"
                "    pass\n\n"
                "s = input()\n"
                "print(reverse_string(s))"
            ),
            "starter_code_javascript": (
                "function reverseString(s) {\n"
                "    // Your code here\n"
                "}\n\n"
                "const s = require('fs').readFileSync('/dev/stdin','utf8').trim();\n"
                "console.log(reverseString(s));"
            ),
            "test_cases": [
                {"input_data": "hello",   "expected_output": "olleh",   "is_hidden": False},
                {"input_data": "world",   "expected_output": "dlrow",   "is_hidden": False},
                {"input_data": "racecar", "expected_output": "racecar", "is_hidden": True},
            ],
        },
        {
            "title": "Merge Intervals",
            "slug": "merge-intervals",
            "description": (
                "Given an array of intervals, merge all overlapping intervals.\n\n"
                "Input: intervals = [[1,3],[2,6],[8,10],[15,18]]\n"
                "Output: [[1,6],[8,10],[15,18]]"
            ),
            "difficulty": "Medium",
            "points_reward": 100,
            "is_practice": True,
            "starter_code_python": (
                "def merge(intervals):\n"
                "    # Your code here\n"
                "    pass\n\n"
                "import json\n"
                "intervals = json.loads(input())\n"
                "print(json.dumps(merge(intervals)))"
            ),
            "starter_code_javascript": (
                "function merge(intervals) {\n"
                "    // Your code here\n"
                "}\n\n"
                "const intervals = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8').trim());\n"
                "console.log(JSON.stringify(merge(intervals)));"
            ),
            "test_cases": [
                {"input_data": "[[1,3],[2,6],[8,10],[15,18]]", "expected_output": "[[1, 6], [8, 10], [15, 18]]", "is_hidden": False},
                {"input_data": "[[1,4],[4,5]]",                 "expected_output": "[[1, 5]]",                    "is_hidden": False},
                {"input_data": "[[1,4],[0,4]]",                 "expected_output": "[[0, 4]]",                    "is_hidden": True},
            ],
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "slug": "longest-substring-no-repeat",
            "description": (
                "Given a string s, find the length of the longest substring "
                "without repeating characters.\n\n"
                "Input: 'abcabcbb'\nOutput: 3\n(The answer is 'abc')"
            ),
            "difficulty": "Medium",
            "points_reward": 100,
            "is_practice": False,
            "starter_code_python": (
                "def length_of_longest_substring(s):\n"
                "    # Your code here\n"
                "    pass\n\n"
                "s = input()\n"
                "print(length_of_longest_substring(s))"
            ),
            "starter_code_javascript": (
                "function lengthOfLongestSubstring(s) {\n"
                "    // Your code here\n"
                "}\n\n"
                "const s = require('fs').readFileSync('/dev/stdin','utf8').trim();\n"
                "console.log(lengthOfLongestSubstring(s));"
            ),
            "test_cases": [
                {"input_data": "abcabcbb", "expected_output": "3", "is_hidden": False},
                {"input_data": "bbbbb",    "expected_output": "1", "is_hidden": False},
                {"input_data": "pwwkew",   "expected_output": "3", "is_hidden": True},
                {"input_data": "",         "expected_output": "0", "is_hidden": True},
            ],
        },
        {
            "title": "Median of Two Sorted Arrays",
            "slug": "median-two-sorted-arrays",
            "description": (
                "Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays.\n\n"
                "The overall run time complexity should be O(log (m+n)).\n\n"
                "Input: nums1 = [1,3], nums2 = [2]\nOutput: 2.0"
            ),
            "difficulty": "Hard",
            "points_reward": 200,
            "is_practice": False,
            "starter_code_python": (
                "def find_median_sorted_arrays(nums1, nums2):\n"
                "    # Your code here\n"
                "    pass\n\n"
                "import json\n"
                "nums1 = json.loads(input())\n"
                "nums2 = json.loads(input())\n"
                "print(find_median_sorted_arrays(nums1, nums2))"
            ),
            "starter_code_javascript": (
                "function findMedianSortedArrays(nums1, nums2) {\n"
                "    // Your code here\n"
                "}\n\n"
                "const lines = require('fs').readFileSync('/dev/stdin','utf8').trim().split('\\n');\n"
                "console.log(findMedianSortedArrays(JSON.parse(lines[0]), JSON.parse(lines[1])));"
            ),
            "test_cases": [
                {"input_data": "[1,3]\n[2]",     "expected_output": "2.0", "is_hidden": False},
                {"input_data": "[1,2]\n[3,4]",   "expected_output": "2.5", "is_hidden": False},
                {"input_data": "[0,0]\n[0,0]",   "expected_output": "0.0", "is_hidden": True},
            ],
        },
    ]

    challenges = []
    for ch_data in challenges_data:
        tc_data = ch_data.pop("test_cases")
        challenge = Challenge(**ch_data)
        db.session.add(challenge)
        db.session.flush()  # get challenge.id

        for tc in tc_data:
            test_case = TestCase(challenge_id=challenge.id, **tc)
            db.session.add(test_case)

        challenges.append(challenge)

    db.session.commit()
    print(f"  ✓ {len(challenges)} challenges seeded with test cases")

    # Create this week's weekly challenge
    weekly = WeeklyChallenge(
        challenge_id=challenges[3].id,   # Merge Intervals
        week_number=1,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
        is_active=True,
    )
    db.session.add(weekly)
    db.session.commit()
    print(f"  ✓ Weekly challenge set: '{challenges[3].title}'")

    return challenges
