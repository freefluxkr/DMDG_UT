import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

class ApiClient {
  // 백엔드 (FastAPI) 주소
  static const String baseUrl = 'http://127.0.0.1:8000';

  static Future<Map<String, dynamic>?> perceive(String agentId, double x, double y, List<String> nearAgents) async {
    try {
      final url = Uri.parse('$baseUrl/agents/$agentId/perceive');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'x': x,
          'y': y,
          'near_agents': nearAgents,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        debugPrint('Perceive Error [${response.statusCode}]: ${response.body}');
      }
    } catch (e) {
      debugPrint('API Error: $e');
    }
    return null;
  }

  static Future<void> sendMemoryEvent({
    required String agentId,
    required String eventType,
    required String sentimentChange,
  }) async {
    try {
      final url = Uri.parse('$baseUrl/agents/$agentId/memory');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'event_type': eventType,
          'sentiment_change': sentimentChange,
        }),
      );
      if (response.statusCode != 200) {
        debugPrint('Memory Event Error: ${response.body}');
      }
    } catch (e) {
      debugPrint('Memory Request Failed: $e');
    }
  }
}
