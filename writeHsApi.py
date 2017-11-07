import sys

def main():
	query = sys.argv[1]

	data = open('./apiKey_template.py', 'r').read()
	data += query + '\''
	file = open('./apiKey.py', 'w')
	file.write(data)
	file.close()

if __name__ == '__main__':
	main()