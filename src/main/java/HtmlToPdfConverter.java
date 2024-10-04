import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class HtmlToPdfConverter {
    public static void main(String[] args) {
        // 範例輸入，可以通過命令列參數或其他方式獲取
        //String inputPath = "https://service.kylab906.com/getreportbyid?DataID=789BB267AB20240924152142";
        String inputPath = "/Users/YM/Desktop/HtmlToPdf/report/report_goodday.html"; // 本地 HTML 檔案路徑
        String outputPdfPath = "output.pdf";
        String wkhtmltopdfPath = "/usr/local/bin/wkhtmltopdf"; // 根據實際安裝路徑修改
        String customCssPath = "/Users/YM/Desktop/HtmlToPdf/css/custom.css"; // 本地 CSS 檔案路徑

        // 檢測輸入路徑是 URL 還是本地檔案
        boolean isURL = isValidURL(inputPath);

        if (isURL) {
            // 處理線上 HTML
            convertUrlToPdf(inputPath, outputPdfPath, wkhtmltopdfPath, customCssPath);
        } else {
            // 處理本地 HTML
            String localHtmlPath = inputPath;
            String processedHtmlPath = "processed_report_goodday.html";

            // 準備資料
            Map<String, String> dataMap = new HashMap<>();
            dataMap.put("UserName", "張三");
            dataMap.put("Technician", "李四");
            dataMap.put("userID", "007F0055");
            dataMap.put("datadate", "2024/09/24");
            dataMap.put("gender", "男");
            dataMap.put("bmi", "22.5");
            dataMap.put("bmi_d","正常");
            dataMap.put("datatime", "10:30 AM");
            dataMap.put("Birthdate", "1990/01/01");
            dataMap.put("Age", "34");
            dataMap.put("XID", "X123456789");
            dataMap.put("HR", "91.8");
            dataMap.put("HR_d", "正常");
            dataMap.put("SD", "21.2");
            dataMap.put("SDNN_d", "正常");
            dataMap.put("RMSSD", "30.5");
            dataMap.put("RMSSD_d", "正常");
            dataMap.put("ANSAGE", "46");
            dataMap.put("ANSAGE_d", "正常");
            dataMap.put("ANS_AVG", "25");
            dataMap.put("ANS_d", "正常");
            dataMap.put("ANS_SD", "5");
            dataMap.put("SYM_AVG", "75");
            dataMap.put("SYM_d", "正常");
            dataMap.put("SYM_SD", "10");
            dataMap.put("VAG_AVG", "65");
            dataMap.put("VAG_d", "正常");
            dataMap.put("VAG_SD", "8");
            dataMap.put("SYM_modulation", "1.0");
            dataMap.put("SYM_modulation_d", "正常");
            dataMap.put("Balance", "0.5");
            dataMap.put("Balance_d", "平衡");
            dataMap.put("TP","487");
            dataMap.put("VL","240");
            dataMap.put("HF","62");
            dataMap.put("LF","177");

            try {
                // 1. 讀取本地 HTML 檔案
                String htmlContent = new String(Files.readAllBytes(Paths.get(localHtmlPath)), StandardCharsets.UTF_8);

                // 2. 替換佔位符
                for (Map.Entry<String, String> entry : dataMap.entrySet()) {
                    String placeholder = "${" + entry.getKey() + "}";
                    htmlContent = htmlContent.replace(placeholder, entry.getValue());
                }

                // 3. 解析 HTML 並注入 <base> 標籤
                Document document = Jsoup.parse(htmlContent);
                Element head = document.head();
                // 注入 <base> 標籤，確保相對路徑資源能夠正確加載
                String baseHref = "file:///Users/YM/Desktop/HtmlToPdf/report/"; // 根據實際路徑調整
                head.prependElement("base").attr("href", baseHref);
                String processedHtmlContent = document.outerHtml();

                // 4. 寫入處理後的 HTML 到臨時檔案
                Files.write(Paths.get(processedHtmlPath), processedHtmlContent.getBytes(StandardCharsets.UTF_8));
                System.out.println("已將處理過的 HTML 寫入本地檔案 " + processedHtmlPath);

                // 5. 轉換處理後的 HTML 為 PDF
                convertLocalHtmlToPdf(processedHtmlPath, outputPdfPath, wkhtmltopdfPath, customCssPath);
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("處理本地 HTML 檔案時發生錯誤。");
            }
        }
    }

    /**
     * 檢測輸入路徑是否為有效的 URL
     *
     * @param urlStr 輸入路徑
     * @return 如果是有效 URL 則返回 true，否則返回 false
     */
    private static boolean isValidURL(String urlStr) {
        try {
            new URL(urlStr).toURI();
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * 使用 wkhtmltopdf 將 URL 轉換為 PDF
     *
     * @param url            線上 HTML 的 URL
     * @param outputPdfPath  輸出 PDF 檔案路徑
     * @param wkhtmltopdfPath wkhtmltopdf 執行檔案路徑
     * @param customCssPath  本地 CSS 檔案路徑
     */
    private static void convertUrlToPdf(String url, String outputPdfPath, String wkhtmltopdfPath, String customCssPath) {
        ProcessBuilder processBuilder = new ProcessBuilder(
                wkhtmltopdfPath,
                "--disable-smart-shrinking",    // 禁用智能縮放
                "--zoom", "0.8",                // 設定縮放比例為 0.8（根據需要調整）
                "--page-size", "A4",            // 設定頁面大小為 A4
                "--margin-top", "1mm",          // 設定頁面邊距
                "--margin-bottom", "1mm",
                "--margin-left", "1mm",
                "--margin-right", "1mm",
                "--enable-local-file-access",   // 允許訪問本地檔案
                "--user-style-sheet", customCssPath, // 注入本地 CSS 檔案
                url,
                outputPdfPath
        );

        try {
            Process process = processBuilder.start();

            // 讀取標準輸出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            // 讀取錯誤輸出
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            while ((line = errorReader.readLine()) != null) {
                System.err.println(line);
            }

            int exitCode = process.waitFor();
            if (exitCode == 0) {
                System.out.println("PDF 轉換成功，檔案路徑: " + outputPdfPath);
            } else {
                System.err.println("PDF 轉換失敗，退出代碼: " + exitCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("轉換 URL 為 PDF 時發生錯誤。");
        }
    }

    /**
     * 使用 wkhtmltopdf 將本地 HTML 檔案轉換為 PDF
     *
     * @param localHtmlPath   本地 HTML 檔案路徑
     * @param outputPdfPath   輸出 PDF 檔案路徑
     * @param wkhtmltopdfPath wkhtmltopdf 執行檔案路徑
     * @param customCssPath   本地 CSS 檔案路徑
     */
    private static void convertLocalHtmlToPdf(String localHtmlPath, String outputPdfPath, String wkhtmltopdfPath, String customCssPath) {
        ProcessBuilder processBuilder = new ProcessBuilder(
                wkhtmltopdfPath,
                "--disable-smart-shrinking",    // 禁用智能縮放
                "--zoom", "0.8",                // 設定縮放比例為 1.0
                "--page-size", "A4",            // 設定頁面大小為 A4
                "--margin-top", "1mm",         // 設定頁面邊距
                "--margin-bottom", "1mm",
                "--margin-left", "1mm",
                "--margin-right", "1mm",
                "--enable-local-file-access",   // 允許訪問本地檔案
                "--user-style-sheet", customCssPath, // 注入本地 CSS 檔案
                localHtmlPath,
                outputPdfPath
        );

        try {
            Process process = processBuilder.start();

            // 讀取標準輸出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            // 讀取錯誤輸出
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            while ((line = errorReader.readLine()) != null) {
                System.err.println(line);
            }

            int exitCode = process.waitFor();
            if (exitCode == 0) {
                System.out.println("PDF 轉換成功，檔案路徑: " + outputPdfPath);
            } else {
                System.err.println("PDF 轉換失敗，退出代碼: " + exitCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("轉換本地 HTML 為 PDF 時發生錯誤。");
        }
    }
}