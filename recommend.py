from recommend.views import Facebook, Naver


def main():
	Naver().update_recommendations()


if __name__ == '__main__':
	main()
