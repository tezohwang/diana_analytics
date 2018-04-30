from recommend.views import RecommendFacebook, RecommendNaver


def main():
    RecommendNaver().update_recommendations()
    RecommendFacebook().update_recommendations()


if __name__ == '__main__':
    main()
