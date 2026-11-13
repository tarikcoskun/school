using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta3;

// listBox1'i 1-500 arasında 20 rastgele sayıyla doldurur.
public partial class Form1_RastgeleSayilar : Window
{
    public Form1_RastgeleSayilar()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        listBox1.Items.Clear();

        Random rastgele = new Random();

        for (int i = 0; i < 20; i++)
        {
            listBox1.Items.Add(rastgele.Next(1, 500));
        }
    }
}
