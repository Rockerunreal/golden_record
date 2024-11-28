import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {

    public static void main(String[] args) throws Exception {
        // Создаем сервер на порту 3000
        HttpServer server = HttpServer.create(new InetSocketAddress(3000), 0);
        server.createContext("/receive", new FilePathHandler());
        server.setExecutor(null); // создает стандартный executor
        server.start();
        System.out.println("Сервер запущен на порту 3000");
    }

    static class FilePathHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equals(exchange.getRequestMethod())) {
                // Читаем тело запроса
                BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
                StringBuilder requestBody = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    requestBody.append(line);
                }

                // Обработка JSON (простой парсинг)
                String jsonBody = requestBody.toString();
                String filePath = null;

                // Извлекаем file_path из JSON
                if (jsonBody.contains("\"file_path\":")) {
                    int startIndex = jsonBody.indexOf("\"file_path\":\"") + "\"file_path\":\"".length();
                    int endIndex = jsonBody.indexOf("\"", startIndex);
                    if (endIndex > startIndex) {
                        filePath = jsonBody.substring(startIndex, endIndex);
                    }
                }

                // Обработка file_path
                if (filePath != null) {
                    System.out.println("Получен file_path: " + filePath);
                    String response = "File path received successfully!";
                    exchange.sendResponseHeaders(200, response.length());
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes());
                    os.close();
                } else {
                    String response = "file_path not found!";
                    exchange.sendResponseHeaders(400, response.length());
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes());
                    os.close();
                }
            } else {
                String response = "Only POST requests are allowed!";
                exchange.sendResponseHeaders(405, response.length());
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            }
        }
    }
}
