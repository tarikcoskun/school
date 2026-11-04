using System;
using System.Globalization;
using Avalonia.Data.Converters;

namespace DersUygulamalari.Hafta6;

// CalendarDatePicker'da tarihi istenen format ve kültürle göstermek için.
public class TarihFormatConverter : IValueConverter
{
    public string Format { get; set; } = "d";
    public string Culture { get; set; } = "";

    private CultureInfo Kultur =>
        string.IsNullOrEmpty(Culture) ? CultureInfo.CurrentCulture : CultureInfo.GetCultureInfo(Culture);

    public object? Convert(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        value switch
        {
            DateTime dt => dt.ToString(Format, Kultur),
            DateTimeOffset dto => dto.ToString(Format, Kultur),
            _ => null
        };

    public object? ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        if (value is not string metin)
            return null;
        if (DateTime.TryParseExact(metin, Format, Kultur, DateTimeStyles.None, out var tarih))
            return tarih;
        if (DateTime.TryParse(metin, Kultur, DateTimeStyles.None, out tarih))
            return tarih;
        return null;
    }
}
