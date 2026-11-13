using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta4;

// textBox1'deki her kelimenin baş harfini büyütür, sonucu label1'e yazar.
public partial class Form2_BasHarfleriBuyutme : Window
{
    public Form2_BasHarfleriBuyutme()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        label1.Text = "";
        foreach (string kelime in textBox1.Text!.Split(" "))
        {
            label1.Text += kelime.Substring(0, 1).ToUpper();
            label1.Text += kelime.Substring(1);
            label1.Text += " ";
        }
    }
}
