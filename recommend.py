from recommend.views import RecommendFacebook, RecommendNaver


def main():
    RecommendFacebook().recommend_for_report()
    RecommendFacebook().update_recommendations()
    RecommendNaver().recommend_for_report()
    RecommendNaver().update_recommendations()


if __name__ == '__main__':
    main()
