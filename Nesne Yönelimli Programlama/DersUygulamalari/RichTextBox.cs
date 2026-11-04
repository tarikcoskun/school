using System;
using Avalonia;
using Avalonia.Controls.Documents;
using Avalonia.Media;
using AvRichTextBox;

namespace DersUygulamalari;

/// <summary>WinForms System.Windows.Forms.RichTextBoxFinds karşılığı (aynı değerler).</summary>
[Flags]
public enum RichTextBoxFinds
{
    None = 0,
    WholeWord = 2,
    MatchCase = 4,
    NoHighlight = 8,
    Reverse = 16,
}

/// <summary>
/// WinForms System.Drawing.Font karşılığı. Size, WinForms'taki gibi punto (pt) cinsindendir.
/// Stil için Avalonia türleri kullanılır: new Font("Consolas", 18f, FontWeight.Bold)
/// </summary>
public class Font(string familyName, float emSize, FontWeight weight = FontWeight.Normal,
    FontStyle style = FontStyle.Normal)
{
    public string Name { get; } = familyName;
    public float Size { get; } = emSize;
    public FontWeight Weight { get; } = weight;
    public FontStyle Style { get; } = style;

    public bool Bold => Weight >= FontWeight.Bold;
    public bool Italic => Style != FontStyle.Normal;

    public override string ToString() => $"[Font: Name={Name}, Size={Size}, Weight={Weight}, Style={Style}]";
}

/// <summary>
/// AvRichTextBox (Simplecto.Avalonia.RichTextBox) üzerine, WinForms RichTextBox API'sine benzeyen ince bir katman.
/// Metin konumları WinForms'taki gibidir: satırlar "\n" ile ayrılır ve her satır sonu tek karakter sayılır.
/// </summary>
public class RichTextBox : AvRichTextBox.RichTextBox
{
    private Font? _font;

    private FlowDocument Doc => FlowDocument;

    // FlowDocument.Text her paragrafın sonuna "\r" koyar; WinForms'ta satır ayırıcı "\n"dir ve sonda yoktur.
    public string Text
    {
        get
        {
            string raw = Doc.Text.Replace('\r', '\n');
            return raw.EndsWith('\n') ? raw[..^1] : raw;
        }
        set
        {
            Doc.ClearBlocks();
            InsertTextAt(0, value ?? "");
            if (_font != null)
                ApplyFont(new TextRange(Doc, 0, Doc.DocEndPoint, false), _font);
            Doc.Select(0, 0);
        }
    }

    public int TextLength => Text.Length;

    public string[] Lines
    {
        get => Text.Split('\n');
        set => Text = string.Join("\n", value);
    }

    public Size Size => Bounds.Size;

    public bool ReadOnly
    {
        get => IsReadOnly;
        set => IsReadOnly = value;
    }

    public Font Font
    {
        get => _font ?? new Font(FontFamily.Name, (float)(FontSize * 72.0 / 96.0));
        set
        {
            _font = value;
            ApplyFont(new TextRange(Doc, 0, Doc.DocEndPoint, false), value);
        }
    }

    // --- Seçim ---

    public int SelectionStart
    {
        get => Doc.Selection.Start;
        set => Select(value, 0);
    }

    public int SelectionLength
    {
        get => Doc.Selection.Length;
        set => Select(SelectionStart, value);
    }

    // Salt okunur: kütüphane, kod ile seçimi değiştirirken bazı durumlarda hata veriyor.
    public string SelectedText
    {
        get
        {
            string text = Text;
            int start = Math.Min(SelectionStart, text.Length);
            return text.Substring(start, Math.Min(SelectionLength, text.Length - start));
        }
    }

    public Color SelectionColor
    {
        get => (Doc.Selection.GetFormatting(Inline.ForegroundProperty) as ISolidColorBrush)?.Color ?? Colors.Black;
        set => Doc.ApplyFormattingOrTypingFormat(Inline.ForegroundProperty, new SolidColorBrush(value));
    }

    public Color SelectionBackColor
    {
        get => (Doc.Selection.GetFormatting(Inline.BackgroundProperty) as ISolidColorBrush)?.Color ?? Colors.Transparent;
        set => Doc.ApplyFormattingOrTypingFormat(Inline.BackgroundProperty, new SolidColorBrush(value));
    }

    public Font SelectionFont
    {
        get
        {
            var sel = Doc.Selection;
            string family = (sel.GetFormatting(Inline.FontFamilyProperty) as FontFamily)?.Name ?? Font.Name;
            double dips = sel.GetFormatting(Inline.FontSizeProperty) is double d ? d : FontSize;
            var weight = sel.GetFormatting(Inline.FontWeightProperty) is FontWeight w ? w : FontWeight.Normal;
            var style = sel.GetFormatting(Inline.FontStyleProperty) is Avalonia.Media.FontStyle s ? s : Avalonia.Media.FontStyle.Normal;
            return new Font(family, (float)(dips * 72.0 / 96.0), weight, style);
        }
        set
        {
            if (SelectionLength > 0)
            {
                ApplyFont(Doc.Selection, value);
                return;
            }
            // Seçim yoksa biçim, yazılacak bir sonraki metne uygulanır.
            Doc.ApplyFormattingOrTypingFormat(Inline.FontFamilyProperty, new FontFamily(value.Name));
            Doc.ApplyFormattingOrTypingFormat(Inline.FontSizeProperty, PointsToDips(value.Size));
            Doc.ApplyFormattingOrTypingFormat(Inline.FontWeightProperty, value.Bold ? FontWeight.Bold : FontWeight.Normal);
            Doc.ApplyFormattingOrTypingFormat(Inline.FontStyleProperty, value.Italic ? Avalonia.Media.FontStyle.Italic : Avalonia.Media.FontStyle.Normal);
        }
    }

    public void Select(int start, int length)
    {
        int max = TextLength;
        start = Math.Clamp(start, 0, max);
        length = Math.Clamp(length, 0, max - start);
        Doc.Select(start, length);
    }

    public void SelectAll() => Select(0, TextLength);

    public void DeselectAll() => Select(SelectionStart, 0);

    // --- Metin işlemleri ---

    public void AppendText(string text)
    {
        int end = InsertTextAt(TextLength, text ?? "");
        Doc.Select(end, 0);
    }

    public void Clear()
    {
        Doc.ClearBlocks();
    }

    /// <summary>WinForms'taki gibi büyük/küçük harf duyarsız arar, bulursa seçer. Bulamazsa -1 döner.</summary>
    public int Find(string str) => Find(str, 0, -1, RichTextBoxFinds.None);

    public int Find(string str, RichTextBoxFinds options) => Find(str, 0, -1, options);

    public int Find(string str, int start, RichTextBoxFinds options) => Find(str, start, -1, options);

    /// <summary>
    /// [start, end) aralığında arar; end = -1 metnin sonu demektir. Bulursa seçer (NoHighlight yoksa),
    /// bulduğu konumu döner; bulamazsa -1 döner.
    /// </summary>
    public int Find(string str, int start, int end, RichTextBoxFinds options)
    {
        ArgumentNullException.ThrowIfNull(str);
        string text = Text;
        if (end < 0 || end > text.Length) end = text.Length;
        if (start < 0 || start > end)
            throw new ArgumentOutOfRangeException(nameof(start));
        if (str.Length == 0 || end - start < str.Length) return -1;

        var comparison = options.HasFlag(RichTextBoxFinds.MatchCase)
            ? StringComparison.Ordinal
            : StringComparison.CurrentCultureIgnoreCase;
        bool reverse = options.HasFlag(RichTextBoxFinds.Reverse);

        int index = reverse
            ? text.LastIndexOf(str, end - 1, end - start, comparison)
            : text.IndexOf(str, start, end - start, comparison);

        while (index >= 0 && options.HasFlag(RichTextBoxFinds.WholeWord) && !IsWholeWord(text, index, str.Length))
        {
            index = reverse
                ? (index - 1 < start ? -1 : text.LastIndexOf(str, index + str.Length - 2, index + str.Length - 1 - start, comparison))
                : (index + 1 > end - str.Length ? -1 : text.IndexOf(str, index + 1, end - index - 1, comparison));
        }

        if (index >= 0 && !options.HasFlag(RichTextBoxFinds.NoHighlight))
            Select(index, str.Length);
        return index;
    }

    private static bool IsWholeWord(string text, int index, int length)
    {
        bool startOk = index == 0 || !char.IsLetterOrDigit(text[index - 1]);
        int after = index + length;
        bool endOk = after >= text.Length || !char.IsLetterOrDigit(text[after]);
        return startOk && endOk;
    }

    public void ScrollToCaret() => Doc.ScrollFlowDocToCaret();

    // --- Yardımcılar ---

    /// <summary>Metni verilen konuma ekler ("\n" yeni paragraf açar) ve eklenen metnin bittiği konumu döner.</summary>
    private int InsertTextAt(int pos, string text)
    {
        string[] parts = text.Replace("\r\n", "\n").Replace('\r', '\n').Split('\n');
        for (int i = 0; i < parts.Length; i++)
        {
            if (i > 0)
            {
                Doc.Select(pos, 0);
                Doc.InsertParagraphAt(pos);
                pos++;
            }
            if (parts[i].Length > 0)
            {
                Doc.SelectHeadless(pos, 0);
                Doc.ReplaceSelectionWithText(parts[i]);
                pos += parts[i].Length;
            }
        }
        return pos;
    }

    private static void ApplyFont(TextRange range, Font font)
    {
        range.ApplyFormatting(Inline.FontFamilyProperty, new FontFamily(font.Name));
        range.ApplyFormatting(Inline.FontSizeProperty, PointsToDips(font.Size));
        ApplyToggle(range, Inline.FontWeightProperty, font.Bold ? FontWeight.Bold : FontWeight.Normal);
        ApplyToggle(range, Inline.FontStyleProperty, font.Italic ? Avalonia.Media.FontStyle.Italic : Avalonia.Media.FontStyle.Normal);
    }

    // Kütüphane kalın/italik için "aç-kapa" mantığı kullanır: tamamı zaten kalınsa Bold uygulamak kalınlığı kaldırır.
    // İlk uygulamadan sonra aralık tek tip olur; istenen değer gelmediyse bir kez daha uygulamak onu çevirir.
    private static void ApplyToggle(TextRange range, AvaloniaProperty property, object value)
    {
        range.ApplyFormatting(property, value);
        if (!Equals(range.GetFormatting(property), value))
            range.ApplyFormatting(property, value);
    }

    // WinForms font boyutu punto, Avalonia ise 1/96 inç (DIP) kullanır.
    private static double PointsToDips(float points) => points * 96.0 / 72.0;
}
