from report.views import ReportFacebook, ReportNaver


def main():
    ReportFacebook().send_report()
    ReportNaver().send_report()


if __name__ == '__main__':
    main()
