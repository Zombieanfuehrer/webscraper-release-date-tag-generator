from _datetime import datetime

class DateFormatter:
    @staticmethod
    def format_date(date_str):
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            raise Exception(f"Failed to parse the date: {date_str}")