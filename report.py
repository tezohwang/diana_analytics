from report.views import ReportFacebook, ReportNaver


def main():
    ReportNaver().send_report()
    ReportFacebook().send_report()


if __name__ == '__main__':
    main()
