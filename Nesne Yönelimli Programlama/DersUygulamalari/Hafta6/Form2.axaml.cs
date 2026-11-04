using System;
using System.Linq;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;

namespace DersUygulamalari.Hafta6;

public partial class Form2 : Window
{
    public Form2()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string aranan = textBox1.Text;
        int i = richTextBox1.Find(aranan, 0, RichTextBoxFinds.MatchCase);
        while (i != -1)
        {
            richTextBox1.SelectionBackColor = Colors.Green;
            i += richTextBox1.Find(aranan, i + aranan.Length, RichTextBoxFinds.MatchCase);
        }
    }
}
