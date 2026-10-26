using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta4;

public partial class Form3 : Window
{
    public Form3()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string[] kelimeler = textBox1.Text.Split(" ");
        Array.Sort(kelimeler, (a, b) => a.Length - b.Length);

        foreach (string kelime in kelimeler)
        {
            listBox1.Items.Add(kelime);
        }
    }
}
