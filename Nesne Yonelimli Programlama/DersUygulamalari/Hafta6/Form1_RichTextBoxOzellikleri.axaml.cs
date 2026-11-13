using System.Linq;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;
using DersUygulamalari.Controls;

namespace DersUygulamalari.Hafta6;

// richTextBox1'in özelliklerini (Lines, Find, Font, seçim renkleri, SelectedText...) dener, sonunda ilk satırı kırmızıyla işaretler.
public partial class Form1_RichTextBoxOzellikleri : Window
{
    public Form1_RichTextBoxOzellikleri()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        label1.Text = richTextBox1.Lines.Count().ToString();
        richTextBox1.SelectionBackColor = Colors.Red;
        richTextBox1.SelectionColor = Colors.Yellow;

        richTextBox1.AppendText("\n" + label1.Text);
        richTextBox1.Font = new Font("Consolas", 18f, FontWeight.Bold);
        label1.Text = richTextBox1.Find("fatih").ToString();
        label1.Text = richTextBox1.Size.Height.ToString();
        label1.Text = richTextBox1.Text;
        label1.Text = richTextBox1.SelectionLength.ToString();
        label1.Text = richTextBox1.SelectedText.Count().ToString();
        // Seçili metin 3 karakterden kısaysa (ör. hiçbir şey seçili değilse) Insert(3) hata verir.
        if (richTextBox1.SelectedText.Length >= 3)
            label1.Text = richTextBox1.SelectedText.Insert(3, "fatih");
        label1.Text = richTextBox1.SelectedText.IndexOf('a').ToString();
        label1.Text = richTextBox1.SelectedText.Replace('a', 'e');
        // label1.Text = richTextBox1.SelectedText.Remove(4);
        // label1.Text = richTextBox1.SelectedText.Remove(4, 3);

        richTextBox1.Select(0, richTextBox1.Lines[0].Length);
        richTextBox1.SelectionBackColor = Colors.Red;
    }
}
