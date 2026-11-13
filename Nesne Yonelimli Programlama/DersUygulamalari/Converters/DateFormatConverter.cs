using System;
using System.Globalization;
using Avalonia.Data.Converters;

namespace DersUygulamalari.Converters;

// CalendarDatePicker'da tarihi istenen format ve kültürle göstermek için.
public class DateFormatConverter : IValueConverter
{
    public string Format { get; set; } = "d";
    public string Culture { get; set; } = "";

    private CultureInfo ResolvedCulture =>
        string.IsNullOrEmpty(Culture) ? CultureInfo.CurrentCulture : CultureInfo.GetCultureInfo(Culture);

    public object? Convert(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        value switch
        {
            DateTime dt => dt.ToString(Format, ResolvedCulture),
            DateTimeOffset dto => dto.ToString(Format, ResolvedCulture),
            _ => null
        };

    public object? ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        if (value is not string text)
            return null;
        if (DateTime.TryParseExact(text, Format, ResolvedCulture, DateTimeStyles.None, out var date))
            return date;
        if (DateTime.TryParse(text, ResolvedCulture, DateTimeStyles.None, out date))
            return date;
        return null;
    }
}
