from recommend.views import RecommendFacebook, RecommendNaver


def main():
    # RecommendNaver().update_recommendations()
    RecommendFacebook().recommend_for_report()


if __name__ == '__main__':
    main()
