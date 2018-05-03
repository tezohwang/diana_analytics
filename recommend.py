from recommend.views import RecommendFacebook, RecommendNaver


def main():
    RecommendFacebook().update_recommendations()
    RecommendNaver().update_recommendations()


if __name__ == '__main__':
    main()
