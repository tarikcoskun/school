using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta4;

public partial class Form2 : Window
{
    public Form2()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        foreach (string kelime in textBox1.Text.Split(" "))
        {
            textBox2.Text += kelime.Substring(0, 1).ToUpper();
            textBox2.Text += kelime.Substring(1);
        }
    }
}
