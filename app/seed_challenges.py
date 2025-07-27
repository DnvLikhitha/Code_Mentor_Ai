import json
from app.models import db, Challenge, UserChallengeProgress

def seed_challenges(app):
    with app.app_context():
        # Delete all progress records first
        UserChallengeProgress.query.delete()
        db.session.commit()
        # Now delete all challenges
        Challenge.query.delete()
        db.session.commit()
        # Now add all challenges
        challenges = [
            Challenge(
                title="Sum Two Numbers",
                description="Write a function that returns the sum of two numbers.",
                starter_code_python="def sum_two_numbers(a, b):\n    # Your code here\n    pass",
                starter_code_cpp="int sumTwoNumbers(int a, int b) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int sumTwoNumbers(int a, int b) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function sumTwoNumbers(a, b) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int SumTwoNumbers(int a, int b) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": [1, 2], "output": 3},
                    {"input": [5, 7], "output": 12}
                ]),
                difficulty="easy"
            ),
            Challenge(
                title="Reverse a String",
                description="Write a function that reverses a string.",
                starter_code_python="def reverse_string(s):\n    # Your code here\n    pass",
                starter_code_cpp="std::string reverseString(std::string s) {\n    // Your code here\n    return \"\";\n}",
                starter_code_java="public String reverseString(String s) {\n    // Your code here\n    return \"\";\n}",
                starter_code_javascript="function reverseString(s) {\n    // Your code here\n    return \"\";\n}",
                starter_code_csharp="public string ReverseString(string s) {\n    // Your code here\n    return \"\";\n}",
                test_cases=json.dumps([
                    {"input": ["hello"], "output": "olleh"},
                    {"input": ["world"], "output": "dlrow"}
                ]),
                difficulty="easy"
            ),
            Challenge(
                title="Find Maximum",
                description="Write a function that returns the maximum of three numbers.",
                starter_code_python="def find_maximum(a, b, c):\n    # Your code here\n    pass",
                starter_code_cpp="int findMaximum(int a, int b, int c) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int findMaximum(int a, int b, int c) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function findMaximum(a, b, c) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int FindMaximum(int a, int b, int c) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": [1, 2, 3], "output": 3},
                    {"input": [10, 5, 7], "output": 10}
                ]),
                difficulty="easy"
            ),
            Challenge(
                title="Palindrome Check",
                description="Write a function that checks if a string is a palindrome.",
                starter_code_python="def is_palindrome(s):\n    # Your code here\n    pass",
                starter_code_cpp="bool isPalindrome(std::string s) {\n    // Your code here\n    return false;\n}",
                starter_code_java="public boolean isPalindrome(String s) {\n    // Your code here\n    return false;\n}",
                starter_code_javascript="function isPalindrome(s) {\n    // Your code here\n    return false;\n}",
                starter_code_csharp="public bool IsPalindrome(string s) {\n    // Your code here\n    return false;\n}",
                test_cases=json.dumps([
                    {"input": ["racecar"], "output": True},
                    {"input": ["hello"], "output": False}
                ]),
                difficulty="easy"
            ),
            Challenge(
                title="Fibonacci Number",
                description="Write a function that returns the nth Fibonacci number.",
                starter_code_python="def fibonacci(n):\n    # Your code here\n    pass",
                starter_code_cpp="int fibonacci(int n) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int fibonacci(int n) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function fibonacci(n) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int Fibonacci(int n) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": [5], "output": 5},
                    {"input": [10], "output": 55}
                ]),
                difficulty="medium"
            ),
            Challenge(
                title="Factorial",
                description="Write a function that returns the factorial of a number.",
                starter_code_python="def factorial(n):\n    # Your code here\n    pass",
                starter_code_cpp="int factorial(int n) {\n    // Your code here\n    return 1;\n}",
                starter_code_java="public int factorial(int n) {\n    // Your code here\n    return 1;\n}",
                starter_code_javascript="function factorial(n) {\n    // Your code here\n    return 1;\n}",
                starter_code_csharp="public int Factorial(int n) {\n    // Your code here\n    return 1;\n}",
                test_cases=json.dumps([
                    {"input": [5], "output": 120},
                    {"input": [0], "output": 1}
                ]),
                difficulty="medium"
            ),
            Challenge(
                title="Count Vowels",
                description="Write a function that counts the number of vowels in a string.",
                starter_code_python="def count_vowels(s):\n    # Your code here\n    pass",
                starter_code_cpp="int countVowels(std::string s) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int countVowels(String s) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function countVowels(s) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int CountVowels(string s) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": ["hello"], "output": 2},
                    {"input": ["sky"], "output": 0}
                ]),
                difficulty="easy"
            ),
            Challenge(
                title="List Intersection",
                description="Write a function that returns the intersection of two lists.",
                starter_code_python="def list_intersection(a, b):\n    # Your code here\n    pass",
                starter_code_cpp="std::vector<int> listIntersection(std::vector<int> a, std::vector<int> b) {\n    // Your code here\n    return {};\n}",
                starter_code_java="public List<Integer> listIntersection(List<Integer> a, List<Integer> b) {\n    // Your code here\n    return new ArrayList<>();\n}",
                starter_code_javascript="function listIntersection(a, b) {\n    // Your code here\n    return [];\n}",
                starter_code_csharp="public List<int> ListIntersection(List<int> a, List<int> b) {\n    // Your code here\n    return new List<int>();\n}",
                test_cases=json.dumps([
                    {"input": [[1,2,3], [2,3,4]], "output": [2,3]},
                    {"input": [[5,6], [7,8]], "output": []}
                ]),
                difficulty="medium"
            ),
            Challenge(
                title="Unique Elements",
                description="Write a function that returns a list of unique elements from the input list.",
                starter_code_python="def unique_elements(lst):\n    # Your code here\n    pass",
                starter_code_cpp="std::vector<int> uniqueElements(std::vector<int> lst) {\n    // Your code here\n    return {};\n}",
                starter_code_java="public List<Integer> uniqueElements(List<Integer> lst) {\n    // Your code here\n    return new ArrayList<>();\n}",
                starter_code_javascript="function uniqueElements(lst) {\n    // Your code here\n    return [];\n}",
                starter_code_csharp="public List<int> UniqueElements(List<int> lst) {\n    // Your code here\n    return new List<int>();\n}",
                test_cases=json.dumps([
                    {"input": [[1,2,2,3,4,4]], "output": [1,2,3,4]},
                    {"input": [[5,5,5,5]], "output": [5]}
                ]),
                difficulty="easy"
            ),
            Challenge(
                title="Anagram Check",
                description="Write a function that checks if two strings are anagrams.",
                starter_code_python="def are_anagrams(s1, s2):\n    # Your code here\n    pass",
                starter_code_cpp="bool areAnagrams(std::string s1, std::string s2) {\n    // Your code here\n    return false;\n}",
                starter_code_java="public boolean areAnagrams(String s1, String s2) {\n    // Your code here\n    return false;\n}",
                starter_code_javascript="function areAnagrams(s1, s2) {\n    // Your code here\n    return false;\n}",
                starter_code_csharp="public bool AreAnagrams(string s1, string s2) {\n    // Your code here\n    return false;\n}",
                test_cases=json.dumps([
                    {"input": ["listen", "silent"], "output": True},
                    {"input": ["hello", "world"], "output": False}
                ]),
                difficulty="medium"
            ),
            # --- Add 6 hard challenges below ---
            Challenge(
                title="Longest Consecutive Sequence",
                description="Given an unsorted array of integers, find the length of the longest consecutive elements sequence.",
                starter_code_python="def longest_consecutive(nums):\n    # Your code here\n    pass",
                starter_code_cpp="int longestConsecutive(std::vector<int>& nums) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int longestConsecutive(int[] nums) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function longestConsecutive(nums) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int LongestConsecutive(int[] nums) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": [[100,4,200,1,3,2]], "output": 4},
                    {"input": [[0,3,7,2,5,8,4,6,0,1]], "output": 9}
                ]),
                difficulty="hard"
            ),
            Challenge(
                title="Word Ladder",
                description="Given two words (beginWord and endWord), and a dictionary's word list, find the length of shortest transformation sequence from beginWord to endWord.",
                starter_code_python="def ladder_length(beginWord, endWord, wordList):\n    # Your code here\n    pass",
                starter_code_cpp="int ladderLength(std::string beginWord, std::string endWord, std::vector<std::string>& wordList) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int ladderLength(String beginWord, String endWord, List<String> wordList) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function ladderLength(beginWord, endWord, wordList) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int LadderLength(string beginWord, string endWord, List<string> wordList) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": ["hit", "cog", ["hot","dot","dog","lot","log","cog"]], "output": 5},
                    {"input": ["hit", "cog", ["hot","dot","dog","lot","log"]], "output": 0}
                ]),
                difficulty="hard"
            ),
            Challenge(
                title="Trapping Rain Water",
                description="Given n non-negative integers representing an elevation map, compute how much water it can trap after raining.",
                starter_code_python="def trap(height):\n    # Your code here\n    pass",
                starter_code_cpp="int trap(std::vector<int>& height) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int trap(int[] height) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function trap(height) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int Trap(int[] height) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": [[0,1,0,2,1,0,1,3,2,1,2,1]], "output": 6},
                    {"input": [[4,2,0,3,2,5]], "output": 9}
                ]),
                difficulty="hard"
            ),
            Challenge(
                title="N-Queens",
                description="The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other. Return all distinct solutions.",
                starter_code_python="def solve_n_queens(n):\n    # Your code here\n    pass",
                starter_code_cpp="std::vector<std::vector<std::string>> solveNQueens(int n) {\n    // Your code here\n    return {};\n}",
                starter_code_java="public List<List<String>> solveNQueens(int n) {\n    // Your code here\n    return new ArrayList<>();\n}",
                starter_code_javascript="function solveNQueens(n) {\n    // Your code here\n    return [];\n}",
                starter_code_csharp="public IList<IList<string>> SolveNQueens(int n) {\n    // Your code here\n    return new List<IList<string>>();\n}",
                test_cases=json.dumps([
                    {"input": [4], "output": 2},
                    {"input": [1], "output": 1}
                ]),
                difficulty="hard"
            ),
            Challenge(
                title="Regular Expression Matching",
                description="Implement regular expression matching with support for '.' and '*'.",
                starter_code_python="def is_match(s, p):\n    # Your code here\n    pass",
                starter_code_cpp="bool isMatch(std::string s, std::string p) {\n    // Your code here\n    return false;\n}",
                starter_code_java="public boolean isMatch(String s, String p) {\n    // Your code here\n    return false;\n}",
                starter_code_javascript="function isMatch(s, p) {\n    // Your code here\n    return false;\n}",
                starter_code_csharp="public bool IsMatch(string s, string p) {\n    // Your code here\n    return false;\n}",
                test_cases=json.dumps([
                    {"input": ["aa", "a"], "output": False},
                    {"input": ["aa", "a*"], "output": True},
                    {"input": ["ab", ".*"], "output": True}
                ]),
                difficulty="hard"
            ),
            Challenge(
                title="Edit Distance",
                description="Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.",
                starter_code_python="def min_distance(word1, word2):\n    # Your code here\n    pass",
                starter_code_cpp="int minDistance(std::string word1, std::string word2) {\n    // Your code here\n    return 0;\n}",
                starter_code_java="public int minDistance(String word1, String word2) {\n    // Your code here\n    return 0;\n}",
                starter_code_javascript="function minDistance(word1, word2) {\n    // Your code here\n    return 0;\n}",
                starter_code_csharp="public int MinDistance(string word1, string word2) {\n    // Your code here\n    return 0;\n}",
                test_cases=json.dumps([
                    {"input": ["horse", "ros"], "output": 3},
                    {"input": ["intention", "execution"], "output": 5}
                ]),
                difficulty="hard"
            ),
        ]
        db.session.bulk_save_objects(challenges)
        db.session.commit()