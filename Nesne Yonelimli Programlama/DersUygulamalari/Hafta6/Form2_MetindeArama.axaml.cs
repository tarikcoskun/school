using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;
using DersUygulamalari.Controls;

namespace DersUygulamalari.Hafta6;

// textBox1'deki metni richTextBox1'de büyük-küçük harfe duyarlı arar, bulduğu her yeri yeşille işaretler.
public partial class Form2_MetindeArama : Window
{
    public Form2_MetindeArama()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string aranan = textBox1.Text ?? "";
        int i = richTextBox1.Find(aranan, 0, RichTextBoxFinds.MatchCase);
        while (i != -1)
        {
            richTextBox1.SelectionBackColor = Colors.LightGreen;
            i = richTextBox1.Find(aranan, i + aranan.Length, RichTextBoxFinds.MatchCase);
        }
    }
}
