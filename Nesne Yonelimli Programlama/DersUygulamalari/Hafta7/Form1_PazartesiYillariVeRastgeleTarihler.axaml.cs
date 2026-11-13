using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta7;

// textBox1-textBox2 arasında 1 Ocak'ı pazartesiye denk gelen yılları listBox1'e yazar.
// textBox3-textBox4 arasında 10 rastgele tarih üretir. tarihleri listBox2'ye, haftanın günlerini listBox3'e yazar.
public partial class Form1_PazartesiYillariVeRastgeleTarihler : Window
{
    public Form1_PazartesiYillariVeRastgeleTarihler()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        int yil_min = Convert.ToInt32(textBox1.Text);
        int yil_max = Convert.ToInt32(textBox2.Text);

        for (int yil = yil_min; yil < yil_max; yil++)
        {
            DateTime yilin_ilk_gunu = new DateTime(yil, 1, 1);
            if (yilin_ilk_gunu.DayOfWeek == DayOfWeek.Monday)
            {
                listBox1.Items.Add(yil);
            }
        }
    }

    private void Button2_Click(object sender, RoutedEventArgs e)
    {
        int yil_min = Convert.ToInt32(textBox3.Text);
        int yil_max = Convert.ToInt32(textBox4.Text);

        Random rastgele = new Random();

        for (int i = 0; i < 10; i++)
        {
            int yil = rastgele.Next(yil_min, yil_max + 1);
            int ay = rastgele.Next(1, 13);
            int gun = rastgele.Next(1, DateTime.DaysInMonth(yil, ay) + 1);

            DateTime rastgele_tarih = new DateTime(yil, ay, gun);
            listBox2.Items.Add(rastgele_tarih);
            listBox3.Items.Add(rastgele_tarih.DayOfWeek);
        }
    }
}
