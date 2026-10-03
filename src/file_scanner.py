import os
ALLOWED_EXTENSIONS = {
    ".js", ".ts", ".py", ".java", ".go",
    ".jsx", ".tsx", ".md", ".json", ".yaml", ".yml"
}

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "venv"
}

def scanRepository(repoPath):
    file = []

    for root,dirs,fileNames in os.walk(repoPath):
        dirs[:] = [
                directory for directory in dirs
                if directory not in IGNORED_DIRECTORIES
            ]


        for fileName in fileNames:
            extension = os.path.splitext(fileName)[1]

            if extension in ALLOWED_EXTENSIONS:
                file.append(os.path.join(root,fileName))

    return file
            

