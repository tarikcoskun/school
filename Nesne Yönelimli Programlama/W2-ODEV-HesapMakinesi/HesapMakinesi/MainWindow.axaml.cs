using System;
using System.Globalization;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace HesapMakinesi;

public partial class MainWindow : Window
{
    // Türkçe ondalık ayracı (virgül) için kültür
    private static readonly CultureInfo Kultur = CultureInfo.GetCultureInfo("tr-TR");

    double sayi1 = 0;
    string islem = "";
    bool yeniSayi = true;

    public MainWindow()
    {
        InitializeComponent();
    }

    private void Buton_Click(object sender, RoutedEventArgs e)
    {
        string tus = ((Button)sender).Content?.ToString() ?? "";

        // Geri tuşu için Unicode ok karakterini "<-" olarak ele al
        if (tus == "\u2190") tus = "<-";

        if (tus.Length > 0 && char.IsDigit(tus[0]))        // 0-9
        {
            if (yeniSayi || txtEkran.Text == "0")
                txtEkran.Text = tus;
            else
                txtEkran.Text += tus;
            yeniSayi = false;
        }
        else if (tus == ",")                                // ondalık
        {
            if (yeniSayi)
            {
                txtEkran.Text = "0,";
                yeniSayi = false;
            }
            else if (!(txtEkran.Text?.Contains(",") ?? false))
                txtEkran.Text += ",";
        }
        else if (tus == "C")                               // temizle
        {
            txtEkran.Text = "0";
            sayi1 = 0;
            islem = "";
            yeniSayi = true;
        }
        else if (tus == "<-")                              // geri sil
        {
            if (!yeniSayi && txtEkran.Text?.Length > 1)
                txtEkran.Text = txtEkran.Text[..^1];
            else
                txtEkran.Text = "0";
        }
        else if (tus == "%")                               // yüzde
        {
            if (double.TryParse(txtEkran.Text, NumberStyles.Any, Kultur, out double d))
                txtEkran.Text = (d / 100).ToString(Kultur);
            yeniSayi = true;
        }
        else if (tus is "+" or "-" or "*" or "/")
        {
            double.TryParse(txtEkran.Text, NumberStyles.Any, Kultur, out sayi1);
            islem = tus;
            yeniSayi = true;
        }
        else if (tus == "=")                               // sonucu göster
        {
            if (islem == "") return;

            double.TryParse(txtEkran.Text, NumberStyles.Any, Kultur, out double sayi2);
            double sonuc = 0;

            switch (islem)
            {
                case "+": sonuc = sayi1 + sayi2; break;
                case "-": sonuc = sayi1 - sayi2; break;
                case "*": sonuc = sayi1 * sayi2; break;
                case "/":
                    if (sayi2 == 0)
                    {
                        txtEkran.Text = "Sıfıra bölünemez!";
                        islem = "";
                        yeniSayi = true;
                        return;
                    }
                    sonuc = sayi1 / sayi2;
                    break;
            }

            txtEkran.Text = sonuc.ToString(Kultur);
            islem = "";
            yeniSayi = true;
        }
    }
}
